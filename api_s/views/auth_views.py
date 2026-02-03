from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import IntegrityError



def cadastro(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("index")
        else:
            return render(request, 'api_s/auth/cadastro.html', {"erro": "Usuário ou senha incorretos."})
    return render(request, 'api_s/auth/cadastro.html')

def register_view(request):
    alerta = None
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password", "").strip()
        if not username or not email or not password:
            alerta = "Preencha todos os campos."
        elif User.objects.filter(username=username).exists():
            alerta = f"Esse usuário já existe."
        elif User.objects.filter(email=email).exists():
            alerta = f"Esse email já está cadastrado."
        else:
            try:
                User.objects.create_user(username=username, email=email, password=password)
                alerta = "Conta criada com sucesso!"
            except IntegrityError:
                alerta = f"O usuário '{username}' ou o email '{email}' já existe."
    return render(request, "api_s/auth/register.html", {"alerta": alerta})

def logout_view(request):
    logout(request)
    return redirect("cadastro")


def teste_login(request):
    return render(request, "api_s/auth/teste_login.html")


# Página de confirmação
def logout_confirm(request):
    return render(request, 'api_s/auth/logout.html')

# Realizar logout
def logout_view(request):
    logout(request)
    return redirect('index')  # ou qualquer página de login/home

                                                        