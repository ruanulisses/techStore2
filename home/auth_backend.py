from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import check_password
from .models import Usuario

class EmailAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            usuario = Usuario.objects.get(email=username)
            if check_password(password, usuario.senha):  # Verifica a senha corretamente
                return usuario
        except Usuario.DoesNotExist:
            return None