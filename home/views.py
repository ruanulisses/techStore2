from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from blog.models import Notificacao,Funcionario # Importando o modelo Produto
from .models import Carrinho, Usuario
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password

from blog.models import Produto,Venda  # Importando o modelo Produto do app estoque
from .models import Usuario  # Importando o modelo Produto do app estoque


# ================ PAGINA INICIAL LOGIN =====================================================
def index(request):
    return render(request, 'home/index.html')

def login_usuario(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        senha = request.POST.get('senha', '').strip()

        if email == 'admin' and senha == 'admin':
            redirect()
            return render(request, 'blog/index.html')

        try:
            usuario = Usuario.objects.get(email=email)  # Tenta obter o usuário pelo email
            if check_password(senha, usuario.senha):  # Verifica a senha criptografada
                request.session['user_id'] = usuario.id
                # messages.success(request, "Login realizado com sucesso como usuário!")
                return redirect('home')  # Redireciona para 'home'
            else:
                pass
                # messages.error(request, "Senha incorreta.")  # Mensagem específica para senha errada

        except Usuario.DoesNotExist:
            messages.error(request, "Usuário não encontrado.")
        # Verificação no banco de dados de funcionários
        try:
            funcionario = Funcionario.objects.get(email=email)
            if check_password(senha, funcionario.senha):
                messages.success(request, "Login realizado com sucesso como funcionário!")
                request.session['funcionario_id'] = funcionario.id
                return render(request, 'blog/inicio.html')
                # return redirect('blog/inicio')  

        except Funcionario.DoesNotExist:
            messages.error(request, "Funcionário não encontrado.")
    
        
    return render(request, 'home/index.html')
    
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
            is_active=True 
        )

        try:    
            usuario.save()
            messages.success(request, "Usuário cadastrado com sucesso!")
            return redirect('index')
        except Exception as e:
            messages.error(request, f"Ocorreu um erro: {str(e)}")
            return render(request, 'home/add.user.html')

    return render(request, 'home/add.user.html')

def admin(request):
    return redirect('blog')
# ============================================================================================


# ================ PAGINA INICIAL HOME ======================================================
def home(request):
    produtos = Produto.objects.all()  # Todos os produtos
    produtos_oferta = Produto.objects.filter(em_oferta=1)  # Produtos em oferta
    
    # Adicionando prints para depuração
    # print(f"Total de produtos: {produtos.count()}")
    # print(f"Total de produtos em oferta: {produtos_oferta.count()}")

    contexto = {
        'produtos': produtos,
        'produtos_oferta': produtos_oferta,
    }
    return render(request, 'home/home.html', contexto)
# ============================================================================================


# ================ PAGINA PRODUTOS ===========================================================
def produtos(request, prod_id):
    prod = Produto.objects.get(id=prod_id)
    contexto = {
        'prod': prod
    }
    return render(request, 'home/acessar.html', contexto)

def produtos_list(request):
    produtos = Produto.objects.all()  # Obtém todos os produtos
    prod = request.GET.get("pesq")
    if prod:
        produtos = produtos.filter(nome__icontains=prod)
    contexto = {
        "nome": "Ruan",
        'produtos': produtos
    }
    return render(request, 'home/produtos.html', contexto) 
# ============================================================================================


# ================ PAGINA CARRINHO ===========================================================
def add_carrinho(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)

    if request.method == 'POST':
        quantidade = int(request.POST.get('quantidade', 1))

        # Verifica se há estoque suficiente
        if quantidade > produto.estoque:
            messages.error(request, f'Estoque insuficiente para {produto.nome}. Disponível: {produto.estoque}.')
            return redirect('produtos_list')  # Redireciona para a lista de produtos

        # Adiciona o produto ao carrinho
        carrinho, created = Carrinho.objects.get_or_create(produto=produto)

        if not created:
            carrinho.quantidade += quantidade
            carrinho.save()
        else:
            carrinho.quantidade = quantidade
            carrinho.save()

        messages.success(request, f'{produto.nome} adicionado ao carrinho com sucesso!')

    # Se não for um POST, redireciona para a lista de produtos
    return redirect('produtos_list')

def carrinho_view(request):
    # Recupera os itens do carrinho
    itens = Carrinho.objects.all()  # Recupera todos os itens do carrinho

    # Calcula o total
    total = sum(item.produto.preco * item.quantidade for item in itens)

    return render(request, 'home/carrinho.html', {'itens': itens, 'total': total})

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
# ============================================================================================


# ================ PAGINA FINALIZAR COMPRA ===================================================
def finalizar_compra(request):
    if request.method == 'POST':
        itens = Carrinho.objects.all() 
        for item in itens:
            # Cria a notificação
            Notificacao.objects.create(
                produto=item.produto.nome,
                quantidade=item.quantidade
            )

            # Registra a venda
            venda = Venda.objects.create(
                produto=item.produto,
                quantidade=item.quantidade,
                total_venda=item.produto.preco * item.quantidade  # Calcula o total da venda
            )

            # Remove o item do carrinho
            item.delete()

        # Limpa a contagem de itens no carrinho
        if 'cart_count' in request.session:
            request.session['cart_count'] = 0
            request.session.modified = True
        
        messages.success(request, 'Compra finalizada com sucesso!')  # Mensagem de sucesso

    return redirect('produtos_list')  # Redireciona para a lista de produtosa
# ============================================================================================


# ================ PAGINA PAGAMENTO ==========================================================
def pagina_pagamento(request):
    return render(request, 'home/pagamento.html')

def pagina_confirmacao(request):
    return render(request, 'home/pagina_confirmacao.html')

def processar_pagamento(request):
    if request.method == 'POST':
        forma_pagamento = request.POST.get('forma_pagamento')
        
        if forma_pagamento == 'cartao':
            messages.success(request, "Pagamento com cartão processado com sucesso!")
        elif forma_pagamento == 'boleto':
            messages.success(request, "Boleto gerado com sucesso!")
        elif forma_pagamento == 'pix':
            messages.success(request, "Pagamento via PIX processado com sucesso!")
        elif forma_pagamento == 'dinheiro':
            messages.success(request, "Pagamento em dinheiro registrado com sucesso!")
        
        return redirect('pagina_confirmacao') 
    
    return redirect('pagina_pagamento')
# ============================================================================================


# ========================= DESCARTE ==========================================================
def contatos(request):
    return render(request, 'home/contato.html')

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

def recuperar_senha(request):

    return render(request, 'home/recuperar_senha.html')