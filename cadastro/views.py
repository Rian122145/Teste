from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

# Create your views here.
def cadastro(request):
    if request.method == 'GET':
        return render(request, 'cadastro.html')
    elif request.method == 'POST':
        nome = request.POST.get('primeiro_nome')
        sobrenome = request.POST.get('sobrenome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        
        # validação de nome e sobrenome
        if not nome or not sobrenome:
            messages.add_message(request, constants.ERROR, 'Os campos nome e sobrenome são obrigatorios')
            return redirect('cadastro')

        # validação de email
        try:
            validate_email(email)
        except ValidationError:
            messages.add_message(request, constants.ERROR, 'E-mail inválido')
            return redirect('cadastro')
        
        # validação de senha
        if not senha == confirmar_senha:
            messages.add_message(request, constants.ERROR, 'As senhas não coincidem')
            return redirect('cadastro')
        
        if len(senha) < 6:
            messages.add_message(request, constants.ERROR, 'A senha deve ter pelo menos 6 caracteres')
            return redirect('cadastro')
        
        try:
            User.objects.get(email=email)
            messages.add_message(request, constants.ERROR, 'E-mail já cadastrado')
            return redirect('cadastro')
        except User.DoesNotExist:
            User.objects.create_user(
                username=email,
                email=email,
                password=senha,
                first_name=nome,
                last_name=sobrenome
            )
            messages.add_message(request, constants.SUCCESS, 'Usuário criado com sucesso')
            return redirect('cadastro')
        

        return
