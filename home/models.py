from django.db import models
from django.utils.timezone import now
from blog.models import Produto
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone

class Usuario(models.Model):
    nome = models.CharField(max_length=100)
    imagem = models.ImageField(upload_to="images/", blank=True, null=True)
    numero = models.CharField(max_length=15)
    email = models.EmailField(max_length=100, unique=True)
    cidade = models.CharField(max_length=100)
    cpf = models.CharField(max_length=14, unique=True)
    idade = models.IntegerField()
    senha = models.CharField(max_length=255)
    data = models.DateTimeField(default=now)
    is_active = models.BooleanField(default=True) 

    def __str__(self):
        return self.nome


class Carrinho(models.Model):
    """Modelo para o carrinho de compras"""
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField(default=1)
    

    def __str__(self):
        return f'{self.produto.nome} - {self.quantidade}'