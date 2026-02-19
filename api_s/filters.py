import django_filters
from api_s.models import Corredor


class CorredorFilter(django_filters.FilterSet): # Cria um filtro de busca para o modelo Corredor usando o pacote django-filter.

    nome = django_filters.CharFilter(
        field_name="nome",
        lookup_expr="icontains",
        label="Nome",

    )

    categoria = django_filters.ChoiceFilter( # Filtro por lista de opções
        field_name="categoria",
        label="Categoria",
        empty_label="Todas",
        
    )

    class Meta:
        model = Corredor
        fields = ["nome", "categoria"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)                                   

        self.filters["categoria"].extra["choices"] = (
            Corredor.objects
            .values_list("categoria", "categoria")
            .distinct()
            .order_by("categoria")
        )
