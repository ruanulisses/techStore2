from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend

class EmailAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            usuario = User.objects.get(email=username)
            if usuario.check_password(password):
                return usuario
        except User.DoesNotExist:
            return None
