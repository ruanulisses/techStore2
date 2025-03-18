from django.db import models
from django import forms
from django.contrib.auth.hashers import make_password, check_password
from datetime import datetime
from decimal import Decimal
from django.utils import timezone


class Postagem(models.Model):
    titulo = models.CharField(max_length=20)
    conteudo = models.TextField(max_length=50)
    imagem = models.ImageField(upload_to="images/", blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Postagens'

    def __str__(self):
        return self.titulo
    

class Comentario(models.Model):
    """Aqui sao aramazendados das postagens"""
    postagem = models.ForeignKey(Postagem, on_delete=models.CASCADE)
    texto = models.TextField(null=False, blank=False)
    data = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Comentarios"

    def __str__(self):
        return self.texto
    

class Produto(models.Model):
    """Aqui são armazenados os Produtos"""
    nome = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=10, decimal_places=2)  # Aumentado para 10
    preco_comprado = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Aumentado para 10
    imagem = models.ImageField(upload_to="images/", blank=True, null=True)
    descricao = models.TextField(max_length=500, blank=True, null=True)  # Aumentado para 500
    estoque = models.IntegerField(default=0)
    data = models.DateTimeField(auto_now_add=True)
    em_oferta = models.BooleanField(default=False)

    def preco_com_desconto(self):
        if self.em_oferta:
            return self.preco * Decimal('0.8')  # Aplica 20% de desconto
        return self.preco
    
    class Meta:
        verbose_name_plural = "produtos"

    def __str__(self):
        return self.nome
    

       
class RegistrosFinanceiro(models.Model):
    produto = models.ForeignKey(Produto, null=True, on_delete=models.SET_NULL)
    mes = models.CharField(max_length=20, default=datetime.now().strftime('%d/%m/%Y'))  # Exemplo: 'Janeiro'
    vendas = models.DecimalField(max_digits=10, decimal_places=2)  # Total de vendas
    despesas = models.DecimalField(max_digits=10, decimal_places=2)  # Total de despesas
    lucro = models.DecimalField(max_digits=10, decimal_places=2)  # Lucro

    def __str__(self):
        return f"{self.mes}: Vendas: {self.vendas}, Despesas: {self.despesas}, Lucro: {self.lucro}"
    

class Notificacao(models.Model):

    produto = models.CharField(max_length=255)  # Nome do produto
    quantidade = models.PositiveIntegerField()  # Quantidade comprada
    data = models.DateTimeField(auto_now_add=True)  # Data da notificação

    def __str__(self):
        return f"{self.quantidade} de {self.produto} em {self.data}"


class Funcionario(models.Model):
    imagem = models.ImageField(upload_to='imagens_funcionarios/', blank=True, null=True)
    nome = models.CharField(max_length=100)
    sobrenome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=15)
    cargo = models.CharField(max_length=100)
    data_nascimento = models.DateField()
    endereco = models.CharField(max_length=255)
    cpf = models.CharField(max_length=11, unique=True)
    rg = models.CharField(max_length=10, unique=True)
    data_admissao = models.DateField()
    salario = models.DecimalField(max_digits=10, decimal_places=2)
    departamento = models.CharField(max_length=100)
    estado_civil = models.CharField(max_length=20)
    data_pagamento = models.DateField(blank=True, null=True)  # Adicionando o campo de data de pagamento
    status_pagamento = models.CharField(max_length=20, default='pendente')
    senha = models.CharField(max_length=128, default='default_password')  # Define a default valueexit

    def __str__(self):
        return f"{self.nome} {self.sobrenome}"

    def set_senha(self, senha):
        self.senha = make_password(senha)  # Armazena a senha de forma segura

    def verificar_senha(self, senha):
        return check_password(senha, self.senha) 

class HistoricoPagamento(models.Model):
    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE)
    valor_pago = models.DecimalField(max_digits=10, decimal_places=2)
    data_pagamento = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.funcionario.nome} - R$ {self.valor_pago} em {self.data_pagamento.strftime('%d/%m/%Y')}"    

class Venda(models.Model):
    """Modelo para registrar vendas de produtos."""
    produto = models.ForeignKey(Produto, related_name='vendas', on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()  # Quantidade vendida
    data_venda = models.DateTimeField(auto_now_add=True)  # Data da venda
    total_venda = models.DecimalField(max_digits=10, decimal_places=2)  # Total da venda (opcional)

    def __str__(self):
        return f"{self.quantidade} de {self.produto.nome} em {self.data_venda}"




