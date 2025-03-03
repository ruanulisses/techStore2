from django.db import models



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
    nome = models.CharField(max_length=20)
    preco = models.DecimalField(max_digits=5, decimal_places=2)
    preco_comprado = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)  # Defina um valor padrão aqui
    imagem = models.ImageField(upload_to="images/", blank=True, null=True)
    descricao = models.TextField(max_length=50, blank=True, null=True)
    estoque = models.IntegerField(default=0)
    data = models.DateTimeField(auto_now_add=True)



    class Meta:
        verbose_name_plural = "produtos"

    def __str__(self):
        return self.nome
       
class RegistrosFinanceiro(models.Model):
    mes = models.DateField(auto_now_add=True)  # Data do registro
    vendas = models.DecimalField(max_digits=10, decimal_places=2)  # Total de vendas
    despesas = models.DecimalField(max_digits=10, decimal_places=2)  # Total de despesas
    lucro = models.DecimalField(max_digits=10, decimal_places=2)  # Lucro

    class Meta:
        verbose_name_plural = "RegistrosFinanceiros"

    def __str__(self):
        return f"{self.mes}: Vendas: {self.vendas}, Despesas: {self.despesas}, Lucro: {self.lucro}"

class Notificacao(models.Model):

    produto = models.CharField(max_length=255)  # Nome do produto
    quantidade = models.PositiveIntegerField()  # Quantidade comprada
    data = models.DateTimeField(auto_now_add=True)  # Data da notificação

    def __str__(self):
        return f"{self.quantidade} de {self.produto} em {self.data}"


