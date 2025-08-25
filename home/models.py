from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from blog.models import Produto
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone


class Perfil(models.Model):
    TIPOS_USUARIO = (
        ('cliente', 'Cliente'),
        ('vendedor', 'Vendedor'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    foto = models.ImageField(upload_to='fotos_perfil/', blank=True, null=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    endereco = models.CharField(max_length=255, blank=True, null=True)
    tipo_usuario = models.CharField(max_length=20, choices=TIPOS_USUARIO, default='cliente')

    # Dados extras do vendedor
    nome_loja = models.CharField(max_length=100, blank=True, null=True)
    descricao_loja = models.TextField(blank=True, null=True)
    documento = models.CharField(max_length=20, blank=True, null=True)  # CPF/CNPJ

    


class Carrinho(models.Model):
    """Modelo para o carrinho de compras"""
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField(default=1)
    

    def __str__(self):
        return f'{self.produto.nome} - {self.quantidade}'
    

class ItemCarrinho(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)


class Pedido(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    itens = models.ManyToManyField('ItemCarrinho')
    total = models.DecimalField(max_digits=10, decimal_places=2)
    data_pedido = models.DateTimeField(auto_now_add=True)  # Este é o campo novo



class ComentarioSite(models.Model):
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    comentario = models.TextField()
    nota = models.PositiveSmallIntegerField()
    data_postagem = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentário de {self.autor.username}"
    


class NotificacaoUsuario(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notificacoes')
    mensagem = models.TextField()
    lida = models.BooleanField(default=False)
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notificação para {self.user.username} - {'Lida' if self.lida else 'Não lida'}"
