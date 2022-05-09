from django import forms
from django.contrib.auth.models import User


class UsuarioForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email')

    def clean(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        if User.objects.filter(username=username).exclude(id=self.instance.id):
            raise forms.ValidationError('O nome de usuário não está disponível')
        if User.objects.filter(email=email).exclude(id=self.instance.id):
            raise forms.ValidationError('O email já foi cadastrado para outro usuário')
