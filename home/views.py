from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from blog.models import  Comentario, Pedido # Importando o modelo Produto
from .models import Carrinho, ItemCarrinho,  NotificacaoUsuario
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
from .forms import ComentarioSiteForm,VendedorForm





def sobre_nos(request):
    return render(request, 'home/sobre_nos.html')


@login_required
def meus_pedidos(request):
    pedidos = Pedido.objects.filter(user=request.user).order_by('-data_criacao')
    notificacoes = request.user.notificacoes.filter(lida=False).order_by('-data_criacao')
    return render(request, 'home/meus_pedidos.html', {'pedidos': pedidos, 'notificacoes': notificacoes})


@login_required
def marcar_notificacoes_lidas(request):
    request.user.notificacoes.filter(lida=False).update(lida=True)
    return redirect('meus_pedidos')


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
import re

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Verifica login rápido para admin fixo
        if username == "ruanadmin" and password == "Admin":
            # Pega o usuário admin existente
            user = User.objects.filter(username="admin").first()
            if user:
                # autentica manualmente usando username e senha
                user = authenticate(request, username=user.username, password="Admin")
                if user:
                    login(request, user)
                return redirect('blog')
            else:
                messages.error(request, "Usuário admin não existe. Crie via createsuperuser.")
                return redirect('login')
        
        # Login normal usando authenticate
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Usuário ou senha inválidos.")
            return redirect('login')

    return render(request, 'home/login_cadastro.html')

def cadastro_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        # Verifica se as senhas coincidem
        if password1 != password2:
            messages.error(request, "As senhas não coincidem.")
            return redirect('cadastro')

        # Verifica se o email já existe
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email já existe.")
            return redirect('cadastro')

        # Verifica se o username já existe
        if User.objects.filter(username=username).exists():
            messages.error(request, "Nome de usuário já existe.")
            return redirect('cadastro')

        # Validação de senha forte
        if len(password1) < 8:
            messages.error(request, "A senha deve ter pelo menos 8 caracteres.")
            return redirect('cadastro')
        if not re.search(r"[0-9]", password1):
            messages.error(request, "A senha deve conter pelo menos um número.")
            return redirect('cadastro')

        # Cria usuário admin se for o email específico
        #Email:ruanadmin
        #Senha:ruan1234
        if email == "Ruanadmin@techstore.com":
            user = User.objects.create_superuser(username=username, email=email, password=password1)
        else:
            user = User.objects.create_user(username=username, email=email, password=password1)

        user.save()

        # Autentica e faz login
        user = authenticate(request, username=username, password=password1)
        if user is not None:
            login(request, user)
            messages.success(request, "Conta criada com sucesso!")
            
            # Redireciona admins para a área de pedidos/blog
            if user.is_superuser:
                return redirect('pedidos_vendedor')
            
            return redirect('home')
        else:
            messages.error(request, "Erro ao autenticar o usuário.")
            return redirect('cadastro')

    return render(request, 'home/login_cadastro.html')


@login_required
def tornar_vendedor(request):
    perfil, _ = Perfil.objects.get_or_create(user=request.user)  # evita erro se não tiver Perfil
    if request.method == 'POST':
        form = VendedorForm(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            p = form.save(commit=False)
            p.tipo_usuario = 'vendedor'
            p.save()
            return redirect('dashboard_vendedor')
    else:
        form = VendedorForm(instance=perfil)
    return render(request, 'home/tornar_vendedor.html', {'form': form})

def dashboard_vendedor(request):
    # Filtra apenas os produtos do usuário logado
    produtos = Produto.objects.filter(vendedor=request.user).order_by('-data')

    # Pesquisa (opcional)
    pesq = request.GET.get('pesq')
    if pesq:
        produtos = produtos.filter(nome__icontains=pesq)

    return render(request, 'blog/inicio.html', {
        'produtos': produtos
    })


def logout_view(request):
    logout(request)
    return redirect('login')

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
            itens = ItemCarrinho.objects.filter(user=request.user)

            if not itens.exists():
                # Se o carrinho estiver vazio, você pode redirecionar ou mostrar erro
                return redirect('carrinho')  # ou outra página

            pedidos_criados = []
            for item in itens:
                produto = item.produto

                # Supondo que você tenha um campo vendedor no Produto, se não tiver, defina outro jeito de pegar
                # vendedor = produto.vendedor if hasattr(produto, 'vendedor') else None
                # if vendedor is None:
                #     # Se não tiver vendedor, pode colocar algum padrão ou retornar erro
                #     # Aqui só um exemplo, coloque seu próprio fluxo
                #     vendedor = User.objects.filter(is_staff=True).first()  # vendedor padrão

                total_item = produto.preco * item.quantidade

                pedido = Pedido.objects.create(
                    user=request.user,
                    # vendedor=vendedor,
                    produto=produto,
                    quantidade=item.quantidade,
                    total=total_item,
                    status='aguardando',
                )
                pedidos_criados.append(pedido)

            # Apaga os itens do carrinho após criar os pedidos
            itens.delete()

            # Se quiser passar o primeiro pedido para a página pix
            return redirect('pagamento_pix', pedido_id=pedidos_criados[0].id)
        
        # Para outros métodos de pagamento, renderize a confirmação normalmente
        return render(request, 'confirmacao.html', {'metodo': metodo})
    
    return render(request, 'home/pagamento.html')

@login_required
def finalizar_compra(request):
    itens = ItemCarrinho.objects.filter(user=request.user)

    for item in itens:
        Pedido.objects.create(
            user=request.user,  # cliente
            
            produto=item.produto,
            quantidade=item.quantidade,
            total=item.produto.preco * item.quantidade,
            status="aguardando"
        )

        # Cria notificação para o vendedor
        NotificacaoUsuario.objects.create(
            usuario=item.produto.vendedor,  # usuário que recebe a notificação
            mensagem=f"Você recebeu um novo pedido para '{item.produto.nome}', quantidade: {item.quantidade}."
        )

    itens.delete()  # limpa carrinho

    messages.success(request, "Compra finalizada! O vendedor foi notificado.")
    return redirect('pagina_confirmacao')

@login_required
def painel_vendedor(request):
    pedidos = Pedido.objects.filter(vendedor=request.user).order_by('-data_criacao')

    if request.method == "POST":
        pedido_id = request.POST.get("pedido_id")
        novo_status = request.POST.get("status")
        pedido = Pedido.objects.get(id=pedido_id, vendedor=request.user)
        pedido.status = novo_status
        pedido.save()
        messages.success(request, "Status do pedido atualizado!")

    return render(request, 'home/painel_vendedor.html', {'pedidos': pedidos})

@login_required
def atualizar_status_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)

    if request.method == 'POST':
        novo_status = request.POST.get('status')
        pedido.status = novo_status
        pedido.save()

        # Criar notificação para o comprador
        NotificacaoUsuario.objects.create(
            usuario=pedido.user,
            mensagem=f"Seu pedido #{pedido.id} agora está: {pedido.get_status_display()}."
        )

        messages.success(request, 'Status do pedido atualizado com sucesso!')
        return redirect('pedidos_vendedor')

    return render(request, 'home/atualizar_status.html', {'pedido': pedido})

@login_required
def minhas_notificacoes(request):
    notificacoes = request.user.notificacoes.order_by('-data_criacao')
    return render(request, 'home/notificacoes.html', {'notificacoes': notificacoes})

def notificacoes_nao_lidas(request):
    if request.user.is_authenticated:
        return {
            'notificacoes_nao_lidas': NotificacaoUsuario.objects.filter(
                usuario=request.user,
                lida=False
            ).count()
        }
    return {}

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


# def finalizar_compra(request):
#     # Lógica para finalizar a compra...
#     # Vamos supor que você tenha a lista de produtos comprados
#     produtos_comprados = carrinho.get_produtos()  # seu método para buscar os produtos

#     for produto in produtos_comprados:
#         Notificacao.objects.create(
#             vendedor=produto.vendedor,  # assumindo que seu modelo Produto tem um campo vendedor
#             produto=produto,
#             mensagem=f"O produto '{produto.nome}' foi vendido!"
#         )

#     # Limpa carrinho e redireciona
#     carrinho.limpar()
#     return redirect('pagina_sucesso')


# def notificacoes_vendedor(request):
#     notificacoes = Notificacao.objects.filter(vendedor=request.user).order_by('-data_criacao')
#     return render(request, 'notificacoes.html', {'notificacoes': notificacoes})


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

    # Agrupar produtos por categoria
    categorias = {}
    for produto in produtos:
        if produto.categoria not in categorias:
            categorias[produto.categoria] = []
        categorias[produto.categoria].append(produto)

    contexto = {
        'categorias': categorias,  # envia agrupado
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

