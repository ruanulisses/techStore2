from django import forms
from django.contrib.auth.models import User
from .models import Perfil
from .models import ComentarioSite

class LoginForm(forms.Form):
    username = forms.CharField(label='Usuário')
    password = forms.CharField(widget=forms.PasswordInput, label='Senha')

class CadastroForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label="Senha")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirme a senha")

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("As senhas não coincidem.")
        return password2

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Esse nome de usuário já está em uso.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError("Esse e-mail já está cadastrado.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])  # criptografa a senha
        if commit:
            user.save()
        return user


class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['foto', 'telefone', 'endereco']



class ComentarioSiteForm(forms.ModelForm):
    class Meta:
        model = ComentarioSite
        fields = ['comentario', 'nota']
        widgets = {
            'comentario': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Escreva seu comentário'}),
            'nota': forms.NumberInput(attrs={'min': 0, 'max': 5, 'step': 0.5}),
        }