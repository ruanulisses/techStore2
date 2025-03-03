from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='blog'),
    path('add_produtos/', views.add_produtos, name='add_produtos'),
    path('produtos/<int:prod_id>/', views.produtos, name='produtos'),
    path('edit_produtos/<int:prod_id>/',views.edit_produtos, name='edit_postagem'),
    path('del_postagem/<int:prod_id>/',views.del_postagem, name='del_postagem'),
    path('comentarios/<int:prod_id>/',views.comentarios, name='comentarios'),
    path('controle_estoque/',views.controle_estoque, name='controle_estoque'),
    path('gestao_financeira/',views.gestao_financeira, name='gestao_financeira'),
    path('salvar-registro/', views.salvar_registro, name='salvar_registro_financeiro'),
    path('relatorio_vendas/', views.relatorio_vendas, name='relatorio_vendas'),
    path('notificacoes/', views.notificacoes_view, name='notificacoes'),
     path('finalizar_compras/', views.finalizar_compras, name='finalizar_compras'),
     path('gestao_financeira/', views.gestao_financeira_view, name='gestao_financeira'),
     
    
]

