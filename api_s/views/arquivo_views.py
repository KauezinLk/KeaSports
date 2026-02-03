from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from api_s.models import ArquivoExcel, Corredor
from ..filters import CorredorFilter


def ArquivoExcelListView(request):
    arquivos = ArquivoExcel.objects.all().order_by('-criado_em')
    return render(request, 'api_s/arquivo/arquivo_list.html', {
        'arquivos': arquivos
    })


def arquivo_detail(request, pk):

    arquivo = get_object_or_404(ArquivoExcel, pk=pk)

    qs = Corredor.objects.filter(
        arquivo=arquivo
    ).order_by('colocacao')

    # aplica o filtro
    filtro = CorredorFilter(request.GET, queryset=qs)

    # pagina o RESULTADO FILTRADO
    paginator = Paginator(filtro.qs, 15)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, 'api_s/arquivo/arquivo_detail.html', {
        'arquivo': arquivo,
        'page': page,
        'filter': filtro,
    })


