from .models import NotificacaoUsuario

def global_context(request):
    notificacoes = []
    if request.user.is_authenticated:
        # Pega as 5 notificações mais recentes do usuário logado
        notificacoes = NotificacaoUsuario.objects.filter(user=request.user).order_by('-data_criacao')[:5]
    return {
        'notificacoes': notificacoes,
    }
