from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from datetime import datetime

from api_s.models import Participante, Corredor, Corrida


def register_view(request):

    alerta = None

    if request.method == "POST":

        nome = request.POST.get("nome_completo", "").strip()

        cpf = request.POST.get("cpf", "").strip()
        cpf = ''.join(filter(str.isdigit, cpf))

        password = request.POST.get("password", "").strip()
        confirmar_senha = request.POST.get("confirmar_senha", "").strip()

        data = request.POST.get("data_nascimento")

        sexo = request.POST.get("sexo", "").strip()
        tamanho_camisa = request.POST.get("tamanho_camisa", "M").strip()
        equipe = request.POST.get("equipe", "").strip() or None

        if not nome or not cpf or not password or not data:
            alerta = "Preencha todos os campos obrigatórios."

        elif not sexo or not tamanho_camisa:
            alerta = "Preencha todos os campos obrigatórios."

        elif password != confirmar_senha:
            alerta = "As senhas não coincidem."

        elif len(cpf) != 11:
            alerta = "CPF inválido."

        elif len(password) < 6:
            alerta = "A senha deve conter pelo menos 6 caracteres."

        elif User.objects.filter(username=cpf).exists():
            alerta = "Esse CPF já está cadastrado."

        else:
            try:
                data_nascimento = datetime.strptime(data, "%Y-%m-%d").date()

                user = User.objects.create_user(
                    username=cpf,
                    password=password,
                    first_name=nome
                )

                corrida = Corrida.objects.first()

                if not corrida:
                    alerta = "Nenhuma corrida cadastrada no sistema."
                    return render(request, "api_s/auth/register.html", {"alerta": alerta})

                Participante.objects.create(
                    usuario=user,
                    nome=nome,
                    cpf=cpf,
                    data_nascimento=data_nascimento,
                    corrida=corrida,
                    sexo=sexo,
                    tamanho_camisa=tamanho_camisa,
                    equipe=equipe
                )

                return redirect("cadastro")

            except IntegrityError:
                alerta = "Erro ao criar conta."

            except ValueError:
                alerta = "Data de nascimento inválida."

    return render(request, "api_s/auth/register.html", {"alerta": alerta})


def cadastro(request):

    if request.method == "POST":

        cpf = request.POST.get("cpf", "").strip()
        cpf = ''.join(filter(str.isdigit, cpf))

        password = request.POST.get("password")

        user = authenticate(request, username=cpf, password=password)

        if user:
            login(request, user)
            return redirect("index")
        else:
            return render(
                request,
                "api_s/auth/cadastro.html",
                {"erro": "CPF ou senha incorretos."}
            )

    return render(request, "api_s/auth/cadastro.html")


@csrf_protect
def auth_page(request):
    """View unificada de autenticação: login para não logados, painel para logados."""
    erro = None
    sucesso = None

    # Se usuário já está logado, exibe painel de logout
    if request.user.is_authenticated:
        participante = None
        try:
            participante = Participante.objects.get(usuario=request.user)
        except Participante.DoesNotExist:
            pass

        if request.method == "POST" and request.POST.get("logout"):
            logout(request)
            return redirect("auth_page")

        return render(
            request,
            "api_s/auth/auth_page.html",
            {
                "usuario_logado": True,
                "participante": participante,
                "sucesso": sucesso
            }
        )

    # Se não está logado, exibe formulário de login
    if request.method == "POST":
        cpf = request.POST.get("cpf", "").strip()
        cpf = ''.join(filter(str.isdigit, cpf))
        password = request.POST.get("password")

        if not cpf or not password:
            erro = "Preencha todos os campos."
        else:
            user = authenticate(request, username=cpf, password=password)

            if user:
                login(request, user)
                # Redireciona com GET para evitar problemas de CSRF no POST
                return redirect("auth_page")
            else:
                erro = "CPF ou senha incorretos."

    return render(
        request,
        "api_s/auth/auth_page.html",
        {"erro": erro}
    )


def historico_usuario(request):

    alerta = None
    historico = None

    if request.method == "POST":

        nome = request.POST.get("nome", "").strip()

        if not nome:
            alerta = "Preencha o campo."
        else:
            historico = Corredor.objects.filter(nome__icontains=nome).order_by("colocacao")

            if not historico.exists():
                alerta = "Nome não encontrado."

    return render(
        request,
        "api_s/participante/historico_usuario.html",
        {
            "historico": historico,
            "alerta": alerta
        }
    )


def buscar_nomes_autocomplete(request):
    """View para autocomplete de nomes de corredores (busca parcial)."""
    termo = request.GET.get("q", "").strip()

    if not termo:
        return JsonResponse({"resultados": []})

    corredores = Corredor.objects.filter(nome__icontains=termo).values_list("nome", flat=True).distinct()[:10]

    return JsonResponse({"resultados": list(corredores)})


def teste_login(request):
    return render(request, "api_s/auth/teste_login.html")


def logout_confirm(request):
    return render(request, "api_s/auth/logout.html")


def logout_view(request):
    logout(request)
    return redirect("index")


@csrf_protect
def logout_rapido(request):
    """View para logout direto via POST, sem página de confirmação."""
    if request.method == "POST":
        logout(request)
    return redirect("index")
