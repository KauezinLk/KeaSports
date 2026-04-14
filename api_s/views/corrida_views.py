from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from api_s.models import Corrida, Participante, Corredor
from api_s.forms import ParticipanteForm
from django.core.paginator import Paginator

import re


def index(request):
    # pega as 3 corridas mais recentes
    corridas = Corrida.objects.all().order_by('-data')[:3]
    return render(request, 'api_s/index.html', {'corridas': corridas})


def listar_corridas(request):
    corridas = Corrida.objects.all()
    return render(request, 'api_s/corrida/listar_corridas.html', {'corridas': corridas})


def resultado_geral(request):
    return render(request, 'api_s/corrida/resultado_geral.html', {
        'teste': 'TESTE'
    })


def validar_cpf(cpf):
    """Valida CPF removendo formatação e verificando dígitos."""
    cpf = re.sub(r'\D', '', cpf)
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False
    # Validação do 1º dígito
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    digito1 = (soma * 10) % 11
    if digito1 == 10:
        digito1 = 0
    if digito1 != int(cpf[9]):
        return False
    # Validação do 2º dígito
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    digito2 = (soma * 10) % 11
    if digito2 == 10:
        digito2 = 0
    if digito2 != int(cpf[10]):
        return False
    return True


def buscar_usuario_cpf(request):
    """Endpoint AJAX para buscar participante pelo CPF."""
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.GET.get('cpf'):
        cpf = request.GET.get('cpf', '').strip()
        cpf_limpo = re.sub(r'\D', '', cpf)

        if not validar_cpf(cpf_limpo):
            return JsonResponse({'encontrado': False, 'erro': 'CPF inválido.'})

        try:
            participante = Participante.objects.get(cpf=cpf_limpo)
            dados = {
                'encontrado': True,
                'nome': participante.nome,
                'data_nascimento': participante.data_nascimento.strftime('%Y-%m-%d') if participante.data_nascimento else '',
                'equipe': participante.equipe or '',
                'sexo': participante.sexo or '',
                'tamanho_camisa': participante.tamanho_camisa or 'M',
                'email': participante.usuario.email if participante.usuario else '',
            }
            return JsonResponse(dados)
        except Participante.DoesNotExist:
            return JsonResponse({'encontrado': False, 'erro': 'CPF não encontrado. Cadastre-se primeiro.'})

    return JsonResponse({'encontrado': False, 'erro': 'Método inválido.'})


def inscrever_corrida(request, corrida_id):
    corrida = get_object_or_404(Corrida, id=corrida_id)

    if request.method == 'POST':
        cpf = request.POST.get('cpf', '').replace('.', '').replace('-', '').strip()

        try:
            participante_existente = Participante.objects.get(cpf=cpf)
            # Usuário encontrado, preencher formulário
            form = ParticipanteForm(request.POST, instance=participante_existente)
        except Participante.DoesNotExist:
            # Usuário não existe, criar novo
            form = ParticipanteForm(request.POST)

        if form.is_valid():
            participante = form.save(commit=False)
            participante.corrida = corrida
            participante.save()
            return render(request, 'api_s/corrida/inscricao_sucesso.html', {'corrida': corrida, 'participante': participante})
    else:
        form = ParticipanteForm()

    return render(request, 'api_s/corrida/inscrever_corrida.html', {
        'form': form,
        'corrida': corrida,
        'buscar_url': 'buscar_usuario_cpf'
    })
