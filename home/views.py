from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from blog.models import Notificacao, Comentario # Importando o modelo Produto
from .models import Carrinho, ItemCarrinho, Pedido
from random import sample
from django.utils import timezone
from blog.models import Produto,Venda  # Importando o modelo Produto do app estoque
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout
from .forms import LoginForm, CadastroForm
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .models import ComentarioSite,Perfil
from .forms import ComentarioSiteForm




def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=username, password=password)
            print(f'Tentando autenticar: {username} / {password}')
            print(f'Usuário retornado pelo authenticate: {user}')

            if user is not None:
                auth_login(request, user)
                messages.success(request, f'Bem-vindo(a) {username}!')
                print(f'logado com sucesso {user}')
                return redirect('home')  # Ajuste para a sua URL de destino após login
            else:
                messages.error(request, 'Usuário ou senha inválidos')
    else:
        form = LoginForm()
    
    return render(request, 'home/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')  # volta pra tela de login


def cadastro_view(request):
    if request.method == 'POST':
        form = CadastroForm(request.POST)
        if form.is_valid():
            user = form.save()  # Salva o usuário com senha corretamente criptografada
            auth_login(request, user)  # Usa o mesmo login aqui
            messages.success(request, 'Cadastro realizado com sucesso!')
            return redirect('home')
        else:
            messages.error(request, 'Erro no cadastro. Verifique os dados.')
    else:
        form = CadastroForm()
    return render(request, 'home/cadastro.html', {'form': form})


@login_required
def configuracoes(request):
    perfil = request.user.perfil
    if request.method == 'POST':
        perfil.telefone = request.POST.get('telefone')
        perfil.endereco = request.POST.get('endereco')
        if 'foto' in request.FILES:
            perfil.foto = request.FILES['foto']
        perfil.save()
        return redirect('configuracoes')

    return render(request, 'home/configuracoes.html', {'perfil': perfil})


@csrf_exempt
@login_required
def adicionar_carrinho_ajax(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        produto_id = data.get('produto_id')
        try:
            produto = Produto.objects.get(id=produto_id)
            item, created = ItemCarrinho.objects.get_or_create(user=request.user, produto=produto)
            if not created:
                item.quantidade += 1
                item.save()
            return JsonResponse({'sucesso': True})
        except Produto.DoesNotExist:
            return JsonResponse({'sucesso': False, 'erro': 'Produto não encontrado'})
    return JsonResponse({'sucesso': False, 'erro': 'Método inválido'})


@login_required
def carrinho(request):
    itens = ItemCarrinho.objects.filter(user=request.user)
    total = sum(item.produto.preco * item.quantidade for item in itens)
    return render(request, 'home/carrinho.html', {'itens': itens, 'total': total})


@login_required
def remover_item_carrinho(request, item_id):
    item = get_object_or_404(ItemCarrinho, id=item_id, user=request.user)
    item.delete()
    return redirect('carrinho')


def pagamento(request):
    if request.method == 'POST':
        metodo = request.POST.get('metodo_pagamento')

        if metodo == 'pix':
            # Criar pedido e redirecionar para o QR Code
            pedido = Pedido.objects.create(user=request.user, total=0)
            itens = ItemCarrinho.objects.filter(user=request.user)

            total = 0
            for item in itens:
                pedido.itens.add(item)
                total += item.produto.preco * item.quantidade

            pedido.total = total
            pedido.save()
            itens.delete()

            return redirect('pagamento_pix', pedido_id=pedido.id)
        
        # Caso seja outro método, renderiza a tela de confirmação normal
        return render(request, 'confirmacao.html', {'metodo': metodo})
    
    return render(request, 'home/pagamento.html')

@login_required
def finalizar_compra(request):
    pedido = Pedido.objects.create(user=request.user, total=0)
    itens = ItemCarrinho.objects.filter(user=request.user)

    total = 0
    for item in itens:
        pedido.itens.add(item)
        total += item.produto.preco * item.quantidade

    pedido.total = total
    pedido.save()
    itens.delete()

    # Simulação de pagamento redirecionando para página com QR Code fake
    return redirect('pagamento_pix', pedido_id=pedido.id)


@csrf_exempt
@login_required
def compra_finalizada(request):
    return render(request, 'home/compra_finalizada.html')


@login_required
def pagamento_pix(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id, user=request.user)
    return render(request, 'home/pagamento_pix.html', {'pedido': pedido})


@login_required(login_url='login')
def perfil_view(request):
    user = request.user
    perfil, created = Perfil.objects.get_or_create(user=user)

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        telefone = request.POST.get('telefone')
        endereco = request.POST.get('endereco')
        foto = request.FILES.get('foto')

        # Atualiza dados do usuário
        user.username = username
        user.email = email
        user.save()

        # Atualiza dados do perfil
        perfil.telefone = telefone
        perfil.endereco = endereco
        if foto:
            perfil.foto = foto
        perfil.save()

        messages.success(request, 'Informações atualizadas com sucesso!')
        return redirect('perfil')  # Substitua pelo nome da sua URL para a view de perfil

    return render(request, 'home/configuracao.html', {
        'user': user,
        'perfil': perfil,
    })



@login_required
def comentarios_site(request):
    if request.method == "POST":
        texto = request.POST.get("texto")
        if texto:
            ComentarioSite.objects.create(autor=request.user, texto=texto)
            return redirect('comentarios_site')  # nome da url para essa view
    
    comentarios = ComentarioSite.objects.all().order_by('-data_postagem')
    return render(request, 'home/comentarios_site.html', {'comentarios': comentarios})


# ================ PAGINA INICIAL LOGIN =====================================================
def index(request):
    return redirect('home')


# ============================================================================================


# ================ PAGINA INICIAL HOME ======================================================
@login_required(login_url='login')
def home(request):
    produtos = Produto.objects.all()
    produto_em_oferta = Produto.objects.filter(em_oferta=True).first()  # Pega só o primeiro

    # Buscar comentários do site para exibir
    comentarios_site = ComentarioSite.objects.all().order_by('-data_postagem')

    if request.method == 'POST':
        form_comentario = ComentarioSiteForm(request.POST, request.FILES)
        if form_comentario.is_valid():
            novo_comentario = form_comentario.save(commit=False)
            novo_comentario.autor = request.user
            novo_comentario.save()
            return redirect('home')  # Evita resubmissão ao atualizar a página
    else:
        form_comentario = ComentarioSiteForm()

    contexto = {
        'produtos': produtos,
        'oferta': produto_em_oferta,
        'comentarios_site': comentarios_site,
        'form_comentario': form_comentario,
    }

    return render(request, 'home/home.html', contexto)
# ============================================================================================


# ================ PAGINA PRODUTOS ===========================================================

def detalhe_produto(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)

    produtos_similares = Produto.objects.filter(
        categoria=produto.categoria
    ).exclude(id=produto.id)[:4]

    produtos_gostaria = Produto.objects.exclude(id=produto.id)[:8]

    comentarios = produto.comentarios.order_by('-data_postagem')[:5]

    if request.method == "POST":
        texto = request.POST.get('texto')
        if texto:
            if request.user.is_authenticated:
                Comentario.objects.create(
                    produto=produto,
                    texto=texto,
                    autor=request.user.username,  # pega o nome do usuário logado
                    data_postagem=timezone.now()
                )
            else:
                messages.warning(request, "Você precisa estar logado para comentar.")
                return redirect('login')

            return redirect('detalhe_produto', produto_id=produto.id)

    context = {
        'produto': produto,
        'produtos_similares': produtos_similares,
        'produtos_gostaria': produtos_gostaria,
        'comentarios': comentarios,
    }

    return render(request, 'home/detalhe_produto.html', context)



def lista_produtos(request):
    produtos = Produto.objects.all()
    prod = request.GET.get("pesq")
    if prod:
        produtos = produtos.filter(nome__icontains=prod)
    contexto = {
        'produtos': produtos,
        'request': request
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
    itens = Carrinho.objects.all()  

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
