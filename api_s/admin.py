# Importa o módulo de administração do Django
from django.contrib import admin
from django.utils.html import format_html
# Importa os modelos
from api_s.models import Corrida, Participante, ArquivoExcel, Corredor


# INLINE PARTICIPANTES (Corrida -> Participantes)

class ParticipanteInline(admin.TabularInline):
    model = Participante
    extra = 1
    fields = (
        'nome',
        'data_nascimento',
        'idade',
        'equipe',
        'cpf',
        'sexo',
        'tamanho_camisa',
        'categoria',
    )
    readonly_fields = ('idade',)


# ADMIN CORRIDA

@admin.register(Corrida)
class CorridaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'data', 'local', 'imagem')
    search_fields = ('nome', 'local')
    inlines = [ParticipanteInline]


# ADMIN PARTICIPANTE

@admin.register(Participante)
class ParticipanteAdmin(admin.ModelAdmin):
    list_display = (
        'nome',
        'idade',
        'equipe',
        'corrida',
        'cpf',
        'sexo',
        'tamanho_camisa',
        'categoria',
    )
    search_fields = ('nome', 'equipe', 'categoria', 'sexo')
    list_filter = ('corrida', 'sexo', 'categoria')

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
