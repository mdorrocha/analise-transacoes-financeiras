import random
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms import modelform_factory
from django.forms.widgets import TextInput
from usuarios.forms import UsuarioForm
from importacoes import utils

@login_required(login_url='login')
def usuarios(request):
    users = User.objects.filter(is_active=True).exclude(username__iexact='admin').order_by('-id')
    return render(request, 'usuarios.html', {'users': users}) 

@login_required(login_url='login')
def cadastrar_usuario(request):
    if request.method == 'GET':
        form = UsuarioForm()
    else:
        form = UsuarioForm(request.POST)
        if form.is_valid():  
            user = form.save(commit=False)
            # gera uma senha aleatória de 6 dígitos
            password = str(random.randrange(pow(10, 5), pow(10, 6)))
            user.set_password(password)        
            user.save()
            utils.enviar_email(user, password)
            messages.add_message(request, messages.SUCCESS, 'Usuário cadastrado com sucesso')
            return redirect('usuarios')
    return render(request, 'cadastrar-usuario.html', {'form': form}) 

@login_required(login_url='login')
def atualizar_usuario(request, id):
    user = User.objects.get(pk=id)
    if user.username == 'Admin':
        messages.add_message(request, messages.ERROR, 'Usuário não encontrado')
        return redirect('usuarios')
    Form = modelform_factory(
        User,
        form=UsuarioForm,
        widgets={'username': TextInput(attrs={'readonly': 'readonly'})}
    ) 
    if request.method == 'GET':        
        form = Form(instance=user)  
    else:
        form = Form(request.POST, instance=user) 
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Usuário atualizado com sucesso')
            return redirect('usuarios')
    return render(request, 'atualizar-usuario.html', {'form': form}) 

@login_required(login_url='login')
def remover_usuario(request, id):
    user = User.objects.get(pk=id)
    if user.username == 'Admin':
        messages.add_message(request, messages.ERROR, 'Usuário não encontrado')
    elif request.user == user:
        messages.add_message(request, messages.ERROR, 'Usuário não pode ser removido')
    else:
        user.is_active = False
        user.save()
        messages.add_message(request, messages.SUCCESS, 'Usuário removido com sucesso')
    return redirect('usuarios')

def get_login(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('importar-arquivo')
    else:
        nome = request.POST.get('usuario')
        senha = request.POST.get('senha')
        user = authenticate(request, username=nome, password=senha)
        if user:
            login(request, user)
            return redirect('importar-arquivo')
        messages.add_message(request, messages.ERROR, 'Suas credenciais estão incorretas')
    return render(request, 'login.html')

def get_logout(request):
    logout(request)
    return redirect('login')

