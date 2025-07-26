from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from blog.models import Produto
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone


class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    foto = models.ImageField(upload_to='fotos_perfil/', blank=True, null=True)
    telefone = models.CharField(max_length=20, blank=True)
    endereco = models.TextField(blank=True)

    def __str__(self):
        return self.user.username


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