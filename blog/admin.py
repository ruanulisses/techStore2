from django.contrib import admin

from .models import Postagem, Comentario, Produto

# Register your models here.


# @admin.register(Postagem)
class PostagemAdmin(admin.ModelAdmin):
    list_display = ['id', 'titulo', 'conteudo']
    list_display_links = ['id']
    list_editable = ['titulo']
    ordering = ['titulo']
    # list_per_page = 3


admin.site.register(Postagem, PostagemAdmin)
admin.site.register(Produto)
