from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='blog'),
    path('add_produtos/', views.add_produtos, name='add_produtos'),
    path('produtos/<int:prod_id>/', views.produtos, name='produtos'),
    path('edit_produtos/<int:prod_id>/', views.edit_produtos, name='edit_produtos'),
    path('del_produto/<int:prod_id>/', views.del_produto, name='del_produto'),
    path('controle_estoque/', views.controle_estoque, name='controle_estoque'),
    path('salvar-registro/', views.salvar_registro, name='salvar_registro_financeiro'),
    path('finalizar_compras/', views.finalizar_compras, name='finalizar_compras'),
    path('gestao_financeira/', views.gestao_financeira_view, name='gestao_financeira'),
    path('relatorio_vendas/', views.relatorio_vendas_view, name='relatorio_vendas'),
    path('funcionarios/adicionar/', views.adicionar_funcionario, name='adicionar_funcionario'),
    path('funcionarios/editar/<int:id>/', views.editar_funcionario, name='editar_funcionario'),  # URL com ID
    path('funcionarios/deletar/<int:id>/', views.deletar_funcionario, name='deletar_funcionario'),
    path('funcionarios/', views.lista_funcionarios, name='lista_funcionarios'),  # URL para listar funcionários
    path('pagamentos/', views.listar_funcionarios_pagamento, name='listar_funcionarios_pagamento'),
    path('pagamento/', views.funcionarios_pagamentos_pendentes, name='funcionarios_pagamentos_pendentes'),
    path('enviar-mensagem/', views.send_payment_message, name='enviar_mensagem'),
    path('produto/<int:produto_id>/oferta/', views.colocar_em_oferta, name='colocar_em_oferta'),
    path('efetuar_pagamento/', views.efetuar_pagamento, name='efetuar_pagamento'),
    path('historico_pagamentos/', views.historico_pagamentos, name='historico_pagamentos'),
   
    path('vendedor/pedidos/', views.pedidos_vendedor, name='pedidos_vendedor'),
    path('vendedor/pedidos/<int:pedido_id>/atualizar/', views.atualizar_status_pedido, name='atualizar_status_pedido'),
    
]