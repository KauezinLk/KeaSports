# Importa o módulo de administração do Django
from django.contrib import admin
from django.utils.html import format_html

# Importa os modelos
from eventos.models import ArquivoExcel, Corredor, Corrida, ImagemBase, Inscricao, Participante


# INLINE INSCRICOES (Corrida -> Participantes)

class InscricaoInline(admin.TabularInline):
    model = Inscricao
    extra = 1
    autocomplete_fields = ('participante',)
    fields = (
        'participante',
        'criada_em',
    )
    readonly_fields = ('criada_em',)


# ADMIN CORRIDA

@admin.register(Corrida)
class CorridaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'data', 'local', 'imagem')
    search_fields = ('nome', 'local')
    inlines = [InscricaoInline]


# ADMIN PARTICIPANTE

@admin.register(Participante)
class ParticipanteAdmin(admin.ModelAdmin):
    list_display = (
        'nome',
        'idade',
        'equipe',
        'cpf',
        'sexo',
        'tamanho_camisa',
        'categoria',
    )
    search_fields = ('nome', 'equipe', 'categoria', 'sexo', 'cpf')
    list_filter = ('sexo', 'categoria')


@admin.register(Inscricao)
class InscricaoAdmin(admin.ModelAdmin):
    list_display = ('participante', 'corrida', 'criada_em')
    autocomplete_fields = ('participante', 'corrida')
    list_filter = ('corrida', 'criada_em')
    search_fields = ('participante__nome', 'participante__cpf', 'corrida__nome')
    ordering = ('-criada_em',)


# ADMIN ARQUIVO EXCEL (COM PREVIEW DE IMAGEM)

@admin.register(ArquivoExcel)
class ArquivoExcelAdmin(admin.ModelAdmin):
    list_display = ('nome', 'data_corrida', 'criado_em', 'preview_imagem')

    def preview_imagem(self, obj):
        if obj.imagem:
            return format_html(
                '<img src="{}" width="120" style="border-radius:6px;" />',
                obj.imagem.url
            )
        return "—"

    preview_imagem.short_description = "Imagem"


# ADMIN CORREDOR

@admin.register(Corredor)
class CorredorAdmin(admin.ModelAdmin):
    list_display = (
        'colocacao',
        'numero',
        'nome',
        'categoria',
        'arquivo',
    )

    search_fields = ('nome', 'numero')
    list_filter = ('arquivo', 'categoria')
    ordering = ('colocacao',)


@admin.register(ImagemBase)
class ImagemBaseAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'ativo', 'preview')
    list_editable = ('ativo',)
    search_fields = ('titulo',)

    def preview(self, obj):
        if obj.imagem:
            return format_html(
                '<img src="{}" width="120" style="border-radius:8px;" />',
                obj.imagem.url
            )
        return "—"

    preview.short_description = "Preview"
