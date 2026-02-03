from django.shortcuts import render
from api_s.models import Participante, Corredor
from rest_framework import viewsets
from api_s.serializers import ParticipanteSerializer


def listar_participantes(request):
    participantes = Participante.objects.select_related('corrida').all()
    return render(request, 'api_s/participante/listar_participantes.html', {'participantes': participantes})

def classificacao_view(request):
    corredores = Corredor.objects.all().order_by('colocacao')
    return render(request, 'api_s/participante/tabela.html', {'corredores': corredores})

class ParticipanteViewSet(viewsets.ModelViewSet):
    queryset = Participante.objects.all()
    serializer_class = ParticipanteSerializer



                                                            




