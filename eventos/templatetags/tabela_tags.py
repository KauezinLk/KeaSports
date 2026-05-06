# tabela_tags.py
from django import template
from ..models import ArquivoExcel

register = template.Library()

@register.inclusion_tag('tabela.html')
def mostrar_tabela(arquivo_id):
    try:
        arquivo = ArquivoExcel.objects.get(id=arquivo_id)
        corredores = arquivo.corredores.all().order_by('colocacao')
    except ArquivoExcel.DoesNotExist:
        corredores = []
    return {'corredores': corredores}
