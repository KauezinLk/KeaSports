from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from api_s.models import ArquivoExcel, Corredor, Participante
from ..filters import CorredorFilter


def ArquivoExcelListView(request):
    arquivos = ArquivoExcel.objects.all().order_by('-criado_em')
    return render(request, 'api_s/arquivo/arquivo_list.html', {
        'arquivos': arquivos # Isso é o que será utilizado no template para acessar os dados dos arquivos.
    })


def arquivo_detail(request, pk):

    arquivo = get_object_or_404(ArquivoExcel, pk=pk) # Busca o arquivo pelo ID ou retorna 404 se não encontrado
    # Utilidade: pk = pk -- Ocorre isso, view recebe que o usuário acessou o arquivo 3, agora o django pega esse id 3 e procura no banco o arquivo de id 3

    qs = Corredor.objects.filter(
        arquivo=arquivo # Mesma lógica de pk=pk, mas aqui é para filtrar os corredores que estão relacionados com o arquivo específico, ou seja, os corredores que pertencem a esse arquivo.
    ).order_by('colocacao')

    filtro = CorredorFilter(request.GET, queryset=qs) # queryset: Puxa os dados do model definido do banco de dados
    # request.GET recebe todos os parâmetros que vêm depois do ? na URL.
    filtroFinal = filtro.qs

    categoria = request.GET.get('categoria') 

    if categoria:
        filtroFinal = filtroFinal.order_by("tempo_segundos")

        for i, corredor in enumerate(filtroFinal, start=1):
            corredor.colocacao_exibicao = i
    else:
        for corredor in filtroFinal:
            corredor.colocacao_exibicao = corredor.colocacao


    # Organizando por paginação
    
    paginator = Paginator(filtroFinal, 10)   # Se eu quiser usar a tabela original uso qs, se quiser usar com os filtros aplicados eu uso filtro.qs
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, 'api_s/arquivo/arquivo_detail.html', {
        'arquivo': arquivo,
        'page': page,
        'filter': filtro,
    })


from django.contrib.auth.decorators import login_required


