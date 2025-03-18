from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Mapeia a URL raiz para a função index
    path('home', views.home, name='home'), 
    path('contatos/', views.contatos, name='contatos'),
    path('produtos/', views.produtos_list, name='produtos_list'), 
    path('cadastrar/', views.cadastrar_usuario, name='cadastrar_usuario'),
    path('login/', views.login_usuario, name='login_usuario'),
    path('admin/', views.admin, name='admin'),
    path('add_carrinho/<int:produto_id>/', views.add_carrinho, name='add_carrinho'),
    path('carrinho/', views.carrinho_view, name='carrinho'),
    path('finalizar_compra/', views.finalizar_compra, name='finalizar_compra'),  # URL para finalizar a compra
    path('remover_item/<int:item_id>/', views.remover_item, name='remover_item'),  # URL para remover item
    path('conta/', views.conta, name='conta'),
    path('produto/', views.produtos, name='produtos'),
    path('pagamento/', views.pagina_pagamento, name='pagina_pagamento'),
    path('processar_pagamento/', views.processar_pagamento, name='processar_pagamento'),
    path('pagina_confirmacao/', views.pagina_confirmacao, name='pagina_confirmacao'),
    path('recuperar_senha/', views.recuperar_senha, name='recuperar_senha'),
    
]
                