from django.shortcuts import render, get_object_or_404, redirect
from api_s.models import Corrida, Participante, Corredor
from api_s.forms import ParticipanteForm
from django.core.paginator import Paginator

from api_s.models import Corrida

def index(request):
    # pega as próximas corridas
    corridas = Corrida.objects.all().order_by('data')[:4]  # limite opcional
    return render(request, 'api_s/index.html', {'corridas': corridas})


def listar_corridas(request):
    corridas = Corrida.objects.all()
    return render(request, 'api_s/corrida/listar_corridas.html', {'corridas': corridas})

def resultado_geral(request):
    return render(request, 'api_s/corrida/resultado_geral.html', {
        'teste': 'TESTE'
    })

def inscrever_corrida(request, corrida_id):
    corrida = get_object_or_404(Corrida, id=corrida_id)
    if request.method == 'POST':
        form = ParticipanteForm(request.POST)
        if form.is_valid():
            participante = form.save(commit=False)
            participante.corrida = corrida
            participante.save()
            return redirect('listar_corridas')
    else:
        form = ParticipanteForm()
    return render(request, 'api_s/corrida/inscrever_corrida.html', {'form': form, 'corrida': corrida})
