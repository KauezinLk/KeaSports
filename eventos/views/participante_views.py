from django.shortcuts import render
from eventos.models import Corredor


def classificacao_view(request):
    corredores = Corredor.objects.all().order_by('colocacao')
    return render(request, 'eventos/participante/tabela.html', {'corredores': corredores})

