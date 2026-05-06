import re

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from eventos.forms import ParticipanteForm
from eventos.models import ArquivoExcel, Corrida, Inscricao, Participante


def index(request):
    corridas = Corrida.objects.all().order_by("-data")[:3]
    resultados_recentes = (
        ArquivoExcel.objects
        .all()
        .order_by("-criado_em")[:9]
    )
    return render(
        request,
        "eventos/index.html",
        {
            "corridas": corridas,
            "resultados_recentes": resultados_recentes,
        },
    )


def listar_corridas(request):
    corridas = Corrida.objects.all()
    return render(request, "eventos/corrida/listar_corridas.html", {"corridas": corridas})


def validar_cpf(cpf):
    cpf = re.sub(r"\D", "", cpf)
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False

    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    digito1 = (soma * 10) % 11
    if digito1 == 10:
        digito1 = 0
    if digito1 != int(cpf[9]):
        return False

    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    digito2 = (soma * 10) % 11
    if digito2 == 10:
        digito2 = 0
    if digito2 != int(cpf[10]):
        return False
    return True


@login_required
def buscar_usuario_cpf(request):
    if request.headers.get("X-Requested-With") == "XMLHttpRequest" or request.GET.get("cpf"):
        cpf = request.GET.get("cpf", "").strip()
        cpf_limpo = re.sub(r"\D", "", cpf)

        if not validar_cpf(cpf_limpo):
            return JsonResponse({"encontrado": False, "erro": "CPF invalido."})

        if not request.user.is_staff and cpf_limpo != request.user.username:
            return JsonResponse(
                {"encontrado": False, "erro": "CPF nao autorizado para este usuario."},
                status=403,
            )

        try:
            participante = Participante.objects.get(cpf=cpf_limpo)
            dados = {
                "encontrado": True,
                "nome": participante.nome,
                "data_nascimento": participante.data_nascimento.strftime("%Y-%m-%d")
                if participante.data_nascimento
                else "",
                "equipe": participante.equipe or "",
                "sexo": participante.sexo or "",
                "tamanho_camisa": participante.tamanho_camisa or "M",
            }
            return JsonResponse(dados)
        except Participante.DoesNotExist:
            return JsonResponse(
                {"encontrado": False, "erro": "CPF nao encontrado. Cadastre-se primeiro."}
            )

    return JsonResponse({"encontrado": False, "erro": "Metodo invalido."})


@login_required
def inscrever_corrida(request, corrida_id):
    corrida = get_object_or_404(Corrida, id=corrida_id)

    if request.method == "POST":
        cpf = re.sub(r"\D", "", request.POST.get("cpf", "").strip())

        if not cpf:
            cpf = request.user.username

        if not validar_cpf(cpf):
            raise PermissionDenied("CPF invalido.")

        if not request.user.is_staff and cpf != request.user.username:
            raise PermissionDenied("Voce nao pode inscrever outro CPF.")

        try:
            participante_existente = Participante.objects.get(cpf=cpf)
            if (
                participante_existente.usuario
                and participante_existente.usuario != request.user
                and not request.user.is_staff
            ):
                raise PermissionDenied("Participante pertence a outro usuario.")
            form = ParticipanteForm(request.POST, instance=participante_existente)
        except Participante.DoesNotExist:
            form = ParticipanteForm(request.POST)

        if form.is_valid():
            with transaction.atomic():
                participante = form.save(commit=False)
                participante.cpf = cpf
                if not participante.usuario_id:
                    participante.usuario = request.user
                participante.save()
                inscricao, criada = Inscricao.objects.get_or_create(
                    participante=participante,
                    corrida=corrida,
                )
            return render(
                request,
                "eventos/corrida/inscricao_sucesso.html",
                {
                    "corrida": corrida,
                    "participante": participante,
                    "inscricao": inscricao,
                    "inscricao_criada": criada,
                },
            )
    else:
        form = ParticipanteForm()

    return render(
        request,
        "eventos/corrida/inscrever_corrida.html",
        {
            "form": form,
            "corrida": corrida,
            "buscar_url": "buscar_usuario_cpf",
        },
    )
