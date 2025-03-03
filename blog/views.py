from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import json


from .models import Postagem, Produto, RegistrosFinanceiro, Notificacao

# Create your views here.


def index(request):
    produtos = Produto.objects.order_by("-id")
    prod = request.GET.get("pesq")
    if prod:
        produtos = produtos.filter(nome__icontains=prod)
    contexto = {
        "nome": "Ruan",
        'produtos': produtos
    }
    return render(request, 'blog/index.html', contexto)

def controle_estoque(request):
    produtos = Produto.objects.order_by("-id")
    contexto = {
        'produtos': produtos
    }
    return render(request, 'blog/controle_estoque.html', contexto)


def gestao_financeira(request):

    return render(request, 'blog/gestao_financeira.html')

def relatorio_vendas(request):

    return render(request, 'blog/relatorio_vendas.html')

@csrf_exempt
def salvar_registro(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        registro = RegistrosFinanceiro(  # Usando o nome correto da classe
            vendas=data['vendas'],
            despesas=data['despesas'],
            lucro=data['lucro']
        )
        registro.save()
        return JsonResponse({'mensagem': 'Registro salvo com sucesso!'})


def listar_registros(request):
    registros = RegistrosFinanceiro.objects.all().values('mes', 'vendas', 'despesas', 'lucro')
    return JsonResponse(list(registros), safe=False)

def produtos(request, prod_id):
    prod = Produto.objects.get(id=prod_id)
    contexto = {
        'prod': prod
    }
    return render(request, 'blog/postagem.html', contexto)


def add_produtos(request):
    if request.method == "POST":
        nome = request.POST.get('nome').strip()
        
        if len(nome) < 8:
            messages.error(request, "Nome muito curto!")
            return redirect('add_produto')

        img = request.FILES.get("imagem")
        descricao = request.POST.get('descricao').strip()
        preco = request.POST.get('preco').strip()
        preco_comprado = request.POST.get('preco_comprado').strip()
        estoque = request.POST.get('estoque').strip()
        
    
        # Se todas as validações passarem, cria o produto
        post = Produto(nome=nome, preco=preco,preco_comprado=preco_comprado ,imagem=img, descricao=descricao, estoque=estoque, )
        messages.success(request, "Produto salvo com sucesso!")
        post.save()
        return redirect('blog')
        

    return render(request, 'blog/add_produto.html')

def edit_produtos(request, prod_id):
    prod = get_object_or_404(Produto, id=prod_id)
    if request.method == "POST":
        nome = request.POST.get('nome').strip()
        preco = request.POST.get('preco').strip()
        descricao = request.POST.get('descricao').strip()
        estoque = request.POST.get('estoque').strip()  
        tipo = request.POST.get('tipo').strip()  
        
        if len(nome) < 8:
            messages.error(request, "nome muito curto!")
            return redirect('edit_produtos', prod_id)
        cont = request.POST.get('cont').strip()
        if len(cont) < 20:
            messages.error(request, "Conteúdo muito curto!")
            return redirect('edit_produtos', prod_id)
        prod.nome = nome
        prod.preco = preco
        prod.descricao = descricao
        prod.estoque = estoque
        prod.tipo = tipo
        prod.save()
        messages.success(request, "produtos editada com sucesso!")
        return redirect('blog')
    contexto = {
        'prod': prod
    }
    return render(request, 'blog/edit_produto.html', contexto)

def del_postagem(request, post_id):
    post = get_object_or_404(Postagem, id=post_id)
    if request.method == "POST":
        post.delete()
        messages.success(request, "Postagem deletada com sucesso!")
        return redirect("blog")
    contexto = {
        'post': post
    }
    return render(request, 'blog/del_postagem.html', contexto)

def comentarios(request, post_id):
    postagem = Postagem.objects.get(id=post_id)
    comentarios = postagem.comentario_set.order_by('-data')
    contexto = {
        'postagens' : postagem,
        'comentarios' : comentarios
    }
    return render(request, 'blog/comentarios.html', contexto)


def notificacoes_view(request):
    notificacoes = Notificacao.objects.all()  # Obtém todas as notificações
    return render(request, 'blog/notificacao_venda.html', {'notificacoes': notificacoes})

def finalizar_compras(request):
    if request.method == 'POST':
        # Obtém todas as notificações
        notificacoes = Notificacao.objects.all()
        
        total_vendas = 0
        total_despesas = 0  # Adicione lógica para calcular despesas, se necessário
        
        for notificacao in notificacoes:
            try:
                # Verifica se o produto existe
                produto = Produto.objects.get(nome=notificacao.produto)
                # Calcula o total de vendas
                total_vendas += notificacao.quantidade * produto.preco
            except Produto.DoesNotExist:
                messages.error(request, f"Produto '{notificacao.produto}' não encontrado.")
                continue  # Ignora a notificação se o produto não for encontrado

        # Aqui você pode adicionar lógica para calcular as despesas, se necessário
        # Exemplo: total_despesas = calcular_despesas(notificacoes)

        # Cria um registro financeiro
        RegistrosFinanceiro.objects.create(
            vendas=total_vendas,
            despesas=total_despesas,
            lucro=total_vendas - total_despesas  # Lucro é vendas - despesas
        )
        
        print(f"Total Vendas: {total_vendas}, Total Despesas: {total_despesas}")
        # Limpa as notificações após finalizar
        Notificacao.objects.all().delete()

        messages.success(request, "Compras finalizadas com sucesso!")
        return redirect('notificacoes')  # Redireciona para a página de notificações

    return redirect('notificacoes')  # Redireciona se não for um POST

def gestao_financeira_view(request):
    # Obtém todos os registros financeiros
    registros = RegistrosFinanceiro.objects.all()
    
    # Calcula os totais
    total_vendas = sum(registro.vendas for registro in registros)
    total_despesas = sum(registro.despesas for registro in registros)
    total_lucro = total_vendas - total_despesas

    return render(request, 'gestao_financeira.html', {
        'total_vendas': total_vendas,
        'total_despesas': total_despesas,
        'total_lucro': total_lucro,
        'registros': registros
    })


    