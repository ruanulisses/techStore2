from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from blog.models import Produto, Notificacao # Importando o modelo Produto
from .models import Carrinho, Usuario
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password

from blog.models import Produto  # Importando o modelo Produto do app estoque
from .models import Usuario  # Importando o modelo Produto do app estoque

def index(request):
    return render(request, 'home/index.html')

def home(request):
    return render(request, 'home/home.html')

def admin(request):
    return redirect('blog')

def produtos_list(request):
    produtos = Produto.objects.all()  # Obtém todos os produtos
    contexto = {
        'produtos': produtos
    }
    return render(request, 'home/produtos.html', contexto) 

def cadastrar_usuario(request):
    if request.method == 'POST':
        nome = request.POST.get('novo_nome').strip()
        foto = request.FILES.get("nova_imagem")
        numero = request.POST.get('novo_numero').strip()
        email = request.POST.get('novo_email').strip()
        cidade = request.POST.get('novo_cidade').strip()
        cpf = request.POST.get('novo_CPF').strip()
        idade = request.POST.get('novo_idade').strip()
        senha = request.POST.get('nova_senha').strip()

        # Verificar se o CPF já existe
        if Usuario.objects.filter(cpf=cpf).exists():
            messages.error(request, "Este CPF já está cadastrado.")
            return render(request, 'home/add.user.html')

        usuario = Usuario(
            nome=nome,
            imagem=foto,
            numero=numero,
            email=email,
            cidade=cidade,
            cpf=cpf,
            idade=idade,
            senha=make_password(senha),  # Salvar senha de forma segura
        )

        try:    
            usuario.save()
            messages.success(request, "Usuário cadastrado com sucesso!")
            return redirect('index')
        except Exception as e:
            messages.error(request, f"Ocorreu um erro: {str(e)}")
            return render(request, 'home/add.user.html')

    return render(request, 'home/add.user.html')


def login_usuario(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        senha = request.POST.get('senha', '').strip()

        if email == 'admin' and senha == 'admin':
            return render(request, 'blog/index.html')

        try:
            usuario = Usuario.objects.get(email=email)
            if check_password(senha, usuario.senha):
                messages.success(request, "Login realizado com sucesso!")
                request.session['user_id'] = usuario.id
                
               

            else:
                messages.error(request, "Usuário ou senha inválidos.")
        except Usuario.DoesNotExist:
            messages.error(request, "Usuário não encontrado.")

    return render(request, 'home/index.html')


def add_carrinho(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)

    if request.method == 'POST':
        quantidade = int(request.POST.get('quantidade', 1))

        # Adiciona o produto ao carrinho
        carrinho, created = Carrinho.objects.get_or_create(produto=produto)

        if not created:
            carrinho.quantidade += quantidade
            carrinho.save()
        else:
            carrinho.quantidade = quantidade
            carrinho.save()

        return redirect('carrinho')  # Redireciona para a página do carrinho

    return redirect('produtos_list')  # Redireciona para a lista de produtos se não for um POST


def carrinho_view(request):
    # Recupera os itens do carrinho
    itens = Carrinho.objects.all()  # Recupera todos os itens do carrinho

    # Calcula o total
    total = sum(item.produto.preco * item.quantidade for item in itens)

    return render(request, 'home/carrinho.html', {'itens': itens, 'total': total})
    

def finalizar_compra(request):
    if request.method == 'POST':
        itens = Carrinho.objects.all() 
        for item in itens:
           
            Notificacao.objects.create(
                produto=item.produto.nome,
                quantidade=item.quantidade
            )
            # Remove o item do carrinho
            item.delete()

        # Limpa a contagem de itens no carrinho
        if 'cart_count' in request.session:
            request.session['cart_count'] = 0
            request.session.modified = True
        
    return redirect('produtos_list') # Renderiza a página de finalização da compra


def remover_item(request, item_id):
    # Obtém o item do carrinho ou retorna 404 se não encontrado
    item = get_object_or_404(Carrinho, id=item_id)
    
    # Remove o item do carrinho
    item.delete()

    # Atualiza a contagem de itens no carrinho
    if 'cart_count' in request.session:
        request.session['cart_count'] -= item.quantidade
        if request.session['cart_count'] < 0:
            request.session['cart_count'] = 0
        request.session.modified = True  # Marca a sessão como modificada

    return redirect('carrinho')  # Redireciona para a página do carrinho



def conta(request):
    # Pegando o usuário logado
    usuario = request.Usuario

    # Pegando os itens do carrinho do usuário
    carrinho = Carrinho.objects.filter(usuario=usuario)

    # Calculando o total da compra
    total = sum(item.produto.preco * item.quantidade for item in carrinho)

    contexto = {
        'usuario': usuario,
        'carrinho': carrinho,
        'total': total
    }

    return render(request, 'conta.html', contexto)
