from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import HttpResponse
from django.db.models import Sum
from django.utils import timezone

from twilio.rest import Client

from .models import Postagem, Produto, RegistrosFinanceiro, Notificacao, Funcionario, HistoricoPagamento

# Create your views here.

# ================ PAGINA HOME =====================================================
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

def colocar_em_oferta(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    produto.em_oferta = not produto.em_oferta  # Alterna o estado de oferta
    produto.save()
    return redirect('blog')

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
        preco = request.POST.get('preco').strip().replace(',', '.') 
        preco_comprado = request.POST.get('preco_comprado').strip().replace(',', '.')
        estoque = request.POST.get('estoque').strip()
        categoria = request.POST.get('categoria').strip()
        
        # Se todas as validações passarem, cria o produto
        post = Produto(nome=nome, preco=float(preco), preco_comprado=float(preco_comprado), imagem=img, descricao=descricao, estoque=int(estoque), categoria=categoria)
        messages.success(request, "Produto salvo com sucesso!")
        post.save()
        return redirect('blog')
        
    return render(request, 'blog/add_produto.html')

def edit_produtos(request, prod_id):
    prod = get_object_or_404(Produto, id=prod_id)
    
    if request.method == "POST":
        nome = request.POST.get('nome').strip()
        preco = request.POST.get('preco').strip().replace(',', '.')  # Substitui vírgula por ponto
        preco_comprado = request.POST.get('preco_comprado').strip().replace(',', '.')  # Substitui vírgula por ponto
        descricao = request.POST.get('descricao').strip()
        estoque = request.POST.get('estoque').strip()   
        categoria = request.POST.get('categoria').strip()   

        # Validação dos campos
        if len(nome) < 8:
            messages.error(request, "Nome muito curto!")
            return redirect('edit_produtos', prod_id)

        if not preco or not preco.replace('.', '', 1).isdigit():
            messages.error(request, "Preço inválido!")
            return redirect('edit_produtos', prod_id)
        
        if not preco_comprado or not preco_comprado.replace('.', '', 1).isdigit():
            messages.error(request, "preco_comprado inválido!")
            return redirect('edit_produtos', prod_id)

        if not estoque.isdigit() or int(estoque) < 0:
            messages.error(request, "Estoque deve ser um número inteiro positivo!")
            return redirect('edit_produtos', prod_id)

        # Atualiza os campos do produto
        prod.nome = nome
        prod.preco = float(preco)  # Converte para float
        prod.preco_comprado = float(preco_comprado)  # Converte para float
        prod.descricao = descricao
        prod.estoque = int(estoque)  # Converte para inteiro
        prod.categoria = categoria  # Converte para inteiro

        # Verifica se uma nova imagem foi enviada
        if request.FILES.get('imagem'):
            prod.imagem = request.FILES['imagem']

        prod.save()
        if prod:
             messages.success(request, "Produto editado com sucesso!")
        return redirect('blog')
    
    contexto = {
        'prod': prod
    }
    
    return render(request, 'blog/edit_produto.html', contexto)

def del_produto(request, prod_id):
    # print(f"Request method: {request.method}")  # Para verificar o método da solicitação
    # print(f"Post ID: {prod_id}")  # Para verificar o ID da postagem
    prod = get_object_or_404(Produto, id=prod_id)
    if request.method == "POST":
        # print("Deletar post...")  # Para verificar se a exclusão está sendo chamada
        prod.delete()
        messages.success(request, "Postagem deletada com sucesso!")
        return redirect("blog")
    contexto = {
        'post': prod
    }
    return render(request, 'blog/del_produto.html', contexto)
# ==================================================================================


# ================ PAGINA ESTOQUE ==================================================
def controle_estoque(request):
    produtos = Produto.objects.order_by("-id")
    contexto = {
        'produtos': produtos
    }
    return render(request, 'blog/controle_estoque.html', contexto)
# ==================================================================================


# ================ PAGINA GESTÃO FINANCEIRA/ RELATORIO DE VENDA ========================================
def gestao_financeira(request):
    return render(request, 'blog/gestao_financeira.html')

def gestao_financeira_view(request):
    # Obtém todos os registros financeiros
    registros = RegistrosFinanceiro.objects.order_by("-mes")  # Ordena por mês, se necessário

    # Inicializa os totais
    total_vendas = sum(registro.vendas for registro in registros)  # Soma todas as vendas
    total_despesas = sum(registro.despesas for registro in registros)  # Soma todas as despesas
    total_lucro = sum(registro.lucro for registro in registros)  # Soma todos os lucros

    contexto = {
        'total_vendas': total_vendas,
        'total_despesas': total_despesas,
        'total_lucro': total_lucro,
        'registros': registros  # Certifique-se de que a chave está correta
    }

    return render(request, 'blog/gestao_financeira.html', contexto)  # O caminho deve corresponder ao local do templat

def relatorio_vendas_view(request):
    registros = RegistrosFinanceiro.objects.all()
    produtos = Produto.objects.all()

    # Filtragem por data
    data_inicio = request.POST.get('dataInicio')
    data_fim = request.POST.get('dataFim')
    produto_id = request.POST.get('produto')
    mes_selecionado = request.POST.get('mes')  # Novo campo para filtrar por mês

    if data_inicio and data_fim:
        registros = registros.filter(mes__range=[data_inicio, data_fim])

    if produto_id:
        registros = registros.filter(produto__id=produto_id)

    if mes_selecionado:
        registros = registros.filter(mes__month=mes_selecionado)  # Filtragem por mês

    # Calcular totais
    total_vendas = sum(float(registro.vendas) for registro in registros)
    total_despesas = sum(float(registro.despesas) for registro in registros)
    total_lucro = sum(float(registro.lucro) for registro in registros)

    # Produtos mais e menos vendidos
    produtos_mais_vendidos = (
        Produto.objects.annotate(total_vendido=Sum('vendas__quantidade'))
        .order_by('-total_vendido')[:5]
    )
    produtos_menos_vendidos = (
        Produto.objects.annotate(total_vendido=Sum('vendas__quantidade'))
        .order_by('total_vendido')[:5]
    )

    # Preparar dados para gráficos
    meses = registros.values_list('mes', flat=True).distinct()  # Obter meses únicos
    vendas = [registro.vendas for registro in registros]
    despesas = [registro.despesas for registro in registros]
    lucros = [registro.lucro for registro in registros]

    contexto = {
        'registros': registros,
        'produtos': produtos,
        'total_vendas': total_vendas,
        'total_despesas': total_despesas,
        'total_lucro': total_lucro,
        'produtos_mais_vendidos': produtos_mais_vendidos,
        'produtos_menos_vendidos': produtos_menos_vendidos,
        'meses': meses,
        'vendas': vendas,
        'despesas': despesas,
        'lucros': lucros,
    }

    return render(request, 'blog/relatorio_vendas.html', contexto)

def listar_registros(request):
    registros = RegistrosFinanceiro.objects.all().values('mes', 'vendas', 'despesas', 'lucro')
    return JsonResponse(list(registros), safe=False)

    # contexto = {
    #     'prod': prod
    # }
    # return render(request, 'blog/edit_produto.html', contexto)
# ==================================================================================


# ================ PAGINA NOTIFICAÇÃO =============================================
def notificacoes_view(request):
    notificacoes = Notificacao.objects.all()  # Obtém todas as notificações
    return render(request, 'blog/notificacao_venda.html', {'notificacoes': notificacoes})

def finalizar_compras(request):
    if request.method == 'POST':
        # Obtém todas as notificações
        notificacoes = Notificacao.objects.all()
        
        total_vendas = 0
        total_despesas = 0
        
        for notificacao in notificacoes:
            try:
                # Verifica se o produto existe
                produto = Produto.objects.get(nome=notificacao.produto)
                
                # Calcula o total de vendas
                total_vendas += notificacao.quantidade * produto.preco
                
                # Calcula o total de despesas
                total_despesas += notificacao.quantidade * produto.preco_comprado
                
                # Atualiza a quantidade do produto
                if produto.estoque >= notificacao.quantidade:
                    produto.estoque -= notificacao.quantidade  # Diminui a quantidade disponível
                    produto.save()  # Salva as alterações no banco de dados
                else:
                    messages.error(request, f"Quantidade insuficiente para o produto '{notificacao.produto}'. Disponível: {produto.estoque}, Solicitado: {notificacao.quantidade}.")
                    continue  # Ignora a notificação se a quantidade for insuficiente

            except Produto.DoesNotExist:
                messages.error(request, f"Produto '{notificacao.produto}' não encontrado.")
                continue  # Ignora a notificação se o produto não for encontrado

        # Cria um registro financeiro após processar todas as notificações
        RegistrosFinanceiro.objects.create(
            vendas=total_vendas,    
            despesas=total_despesas,
            lucro=total_vendas - total_despesas  # Lucro é vendas - despesas
        )
        
        # Limpa as notificações após finalizar
        Notificacao.objects.all().delete()

        messages.success(request, "Compras finalizadas com sucesso!")
        return redirect('notificacoes')  # Redireciona para a página de notificações

    return redirect('notificacoes')  # Redireciona se não for um POST

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

# ==================================================================================


# ================ PAGINA FUCIONARIOS =============================================
def adicionar_funcionario(request):
    if request.method == 'POST':
        funcionario = Funcionario(
            imagem=request.FILES.get('imagem'),
            nome=request.POST.get('nome'),
            sobrenome=request.POST.get('sobrenome'),
            email=request.POST.get('email'),
            telefone=request.POST.get('telefone'),
            cargo=request.POST.get('cargo'),
            data_nascimento=request.POST.get('data_nascimento'),
            endereco=request.POST.get('endereco'),
            cpf=request.POST.get('cpf'),
            rg=request.POST.get('rg'),
            data_admissao=request.POST.get('data_admissao'),
            salario=request.POST.get('salario'),
            departamento=request.POST.get('departamento'),
            estado_civil=request.POST.get('estado_civil'),
            data_pagamento=request.POST.get('data_pagamento'),
        )
        funcionario.set_senha(request.POST.get('senha'))  # Define a senha de forma segura
        funcionario.save()
        return redirect('lista_funcionarios')  # Redireciona para a lista de funcionários

    return render(request, 'blog/add_funcionario.html')

def lista_funcionarios(request):
    funcionarios = Funcionario.objects.order_by("-id")  # Obtém todos os funcionários
    func = request.GET.get("func")
    if func:
        funcionarios = funcionarios.filter(nome__icontains=func)  # Filtra funcionários pelo nome
    contexto = {
        "nome": "func",
        'funcionarios': funcionarios
    }
    return render(request, 'blog/funcionario.html', contexto) 

from decimal import Decimal
def editar_funcionario(request, id):
    funcionario = get_object_or_404(Funcionario, id=id)

    if request.method == 'POST':
        # Atualiza os campos do funcionário
    
        funcionario.nome = request.POST.get('nome')
        funcionario.sobrenome = request.POST.get('sobrenome')
        funcionario.email = request.POST.get('email')
        funcionario.telefone = request.POST.get('telefone')
        funcionario.cargo = request.POST.get('cargo')
        funcionario.data_nascimento = request.POST.get('data_nascimento')
        funcionario.endereco = request.POST.get('endereco')
        funcionario.cpf = request.POST.get('cpf')
        funcionario.rg = request.POST.get('rg')
        funcionario.data_admissao = request.POST.get('data_admissao')
        funcionario.salario = request.POST.get('salario')
        funcionario.departamento = request.POST.get('departamento')
        funcionario.estado_civil = request.POST.get('estado_civil')
        funcionario.data_pagamento = request.POST.get('data_pagamento')

        # Verifica se uma nova imagem foi enviada
        if request.FILES.get('imagem'):
            funcionario.imagem = request.FILES['imagem']

        # Define a senha de forma segura
        if request.POST.get('senha'):
            funcionario.set_senha(request.POST.get('senha'))

        funcionario.save()  # Salva as alterações
        return redirect('lista_funcionarios')  # Redireciona para a lista de funcionários

    contexto = {
        'funcionario': funcionario
    }
    return render(request, 'blog\editar_fucionario.html', contexto)

def deletar_funcionario(request, id):
    funcionario = get_object_or_404(Funcionario, id=id)
    if request.method == 'POST':
        funcionario.delete()
        return redirect('lista_funcionarios')
       
    return render(request,'blog/funcionario.html',{'funcionario': funcionario})
# ==================================================================================


# ================ PAGINA PAGAMETO DOS FUCIONARIOS =================================
def listar_funcionarios_pagamento(request):
    # Obtendo a data atual
    data_atual = timezone.now().date()

    # Consultando todos os funcionários e ordenando pela data de pagamento
    funcionarios_proximos_pagamento = Funcionario.objects.filter(data_pagamento__gte=data_atual).order_by('data_pagamento')

    return render(request, 'blog/pagamentos.html', {'funcionarios': funcionarios_proximos_pagamento})

def send_payment_message(request):
    if request.method == 'POST':
        funcionario_id = request.POST.get('funcionario_id')  # Supondo que você tenha o ID do funcionário
        funcionario = get_object_or_404(Funcionario, id=funcionario_id)

        # Mensagem a ser enviada
        message = f"Olá {funcionario.nome}, seu pagamento foi efetuado."

        # Enviar a mensagem
       
        return HttpResponse('Mensagem enviada com sucesso!')

    return render(request, 'pagamentos.html')

from datetime import datetime, timedelta

def funcionarios_pagamentos_pendentes(request):
    funcionarios = Funcionario.objects.all()
    funcionarios_com_pagamento_pendente = []

    # Obtém a data atual
    data_atual = datetime.now()

    for funcionario in funcionarios:
        # Verifica se o funcionário tem uma data de pagamento
        if funcionario.data_pagamento:
            # Verifica se o pagamento foi feito no mês atual
            if funcionario.data_pagamento.month == data_atual.month and funcionario.data_pagamento.year == data_atual.year:
                funcionario.status_pagamento = "Pagamento Efetuado"
            else:
                # Verifica se o pagamento foi feito no mês anterior
                if funcionario.data_pagamento >= (data_atual - timedelta(days=30)):
                    funcionario.status_pagamento = "Pagamento Efetuado"
                else:
                    funcionario.status_pagamento = "Pagamento Pendente"
        else:
            funcionario.status_pagamento = "Pagamento Pendente"

        # Adiciona o funcionário à lista com o status atualizado
        funcionarios_com_pagamento_pendente.append(funcionario)

    # Obter o histórico de pagamentos
    historicos = HistoricoPagamento.objects.all().order_by('-data_pagamento')

    return render(request, 'pagamentos.html', {
        'funcionarios': funcionarios_com_pagamento_pendente,
        'historicos': historicos
    })

def efetuar_pagamento(request):
    if request.method == 'POST':
        funcionario_id = request.POST.get('funcionario_id')
        funcionario = get_object_or_404(Funcionario, id=funcionario_id)

        # Deduzir o salário do lucro da loja
        registro_financeiro = RegistrosFinanceiro.objects.first()  # Supondo que haja apenas um registro financeiro
        if registro_financeiro:
            registro_financeiro.lucro -= funcionario.salario
            registro_financeiro.save()

        # Atualizar ou criar o registro financeiro para o mês atual
        mes_atual = timezone.now().date().strftime('%B')  # Obtém o nome do mês atual
        ano_atual = timezone.now().year

        # Obter ou criar o registro financeiro para o mês atual
        registro_financeiro, created = RegistrosFinanceiro.objects.get_or_create(
            mes=mes_atual,  # Use o campo correto aqui
            defaults={'vendas': 0.00, 'despesas': 0.00, 'lucro': 0.00}
        )

        # Atualizar as despesas e o lucro
        registro_financeiro.despesas += funcionario.salario
        registro_financeiro.lucro = registro_financeiro.vendas - registro_financeiro.despesas
        registro_financeiro.save()

        # Registrar o pagamento no histórico
        historico_pagamento = HistoricoPagamento(
            funcionario=funcionario,
            valor_pago=funcionario.salario
        )
        historico_pagamento.save()

        # Atualizar a data de pagamento do funcionário
        funcionario.data_pagamento = timezone.now()
        funcionario.status_pagamento = 'pago'  # Atualiza o status de pagamento
        funcionario.save()  # Salva as alterações no funcionário

        return redirect('listar_funcionarios_pagamento')  # Redireciona para a página de pagamentos

    return render(request, 'pagamentos.html')
  
def historico_pagamentos(request):
    historicos = HistoricoPagamento.objects.all().order_by('-data_pagamento')
    return render(request, 'blog/pagamentos.html', {'historicos': historicos})
# ==================================================================================














