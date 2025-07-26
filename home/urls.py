from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Mapeia a URL raiz para a função index
    path('cadastro/', views.cadastro_view, name='cadastro'),
    path('home', views.home, name='home'), 
     path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('produtos/', views.lista_produtos, name='produtos'), 
    path('finalizar-compra/', views.finalizar_compra, name='finalizar_compra'),
    path('pagamento_pix/', views.pagamento_pix, name='pagamento_pix'),
    path('remover-item/<int:item_id>/', views.remover_item_carrinho, name='remover_item_carrinho'),
    path('produto/<int:produto_id>/', views.detalhe_produto, name='detalhe_produto'),
    path('adicionar-carrinho-ajax/', views.adicionar_carrinho_ajax, name='adicionar_carrinho_ajax'),
    path('carrinho/', views.carrinho, name='carrinho'),
    path('finalizar-compra/', views.finalizar_compra, name='finalizar_compra'),
    path('pagamento-pix/<int:pedido_id>/', views.pagamento_pix, name='pagamento_pix'),
    path('compra-finalizada/', views.compra_finalizada, name='compra_finalizada'),
    path('pagamento/', views.pagamento, name='pagamento'),
    path('perfil/', views.perfil_view, name='perfil'),
]
                