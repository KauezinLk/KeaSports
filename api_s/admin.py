#Importa o módulo de administração do Django, usado para configurar o painel administrativo.
from django.contrib import admin 
from api_s.models import Corrida, Participante, ArquivoExcel, Corredor

# Inline: Permite que você edite ou adicione objetos “filhos” diretamente dentro da página do objeto “pai” no painel admin, CORRIDA --> PARTICIPANTES.
class ParticipanteInline(admin.TabularInline): # TabularInline: Mostrar e editar apenas filhos dentro do pai, em formato de tabela.
    model = Participante # Define o modelo Participante como o modelo filho a ser exibido inline dentro do modelo Corrida.
    # É um atributo predefinido do Django
    extra = 1  # Faz aparecer um campo extra vazio para adicionar um novo participante. Atributo pré definido do Django.
    fields = ('nome', 'data_nascimento', 'idade', 'equipe', 'cpf', 'sexo', 'tamanho_camisa', 'categoria') 
    # Define quais campos do modelo Participante serão exibidos no admin dentro da corrida.
    readonly_fields = ('idade',)  # Define o campo idade como somente leitura (não pode ser editado)

class CorredorInline(admin.TabularInline):
    model = Corredor
    extra = 0
    fields = ('colocacao', 'numero', 'nome', 'categoria', 'equipe', 'tempo_segundos', 'Vel_media', 'tempo_formatado')
    ordering = ('colocacao',) # Ordena por colocação crescente

@admin.register(Corrida) # Registrar Corrida
class CorridaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'data', 'local') # Campos exibidos na lista de corridas
    search_fields = ('nome', 'local') # Campos pesquisáveis
   
# Registrar Participante (opcional, para pesquisa separada)
@admin.register(Participante)
class ParticipanteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'idade', 'equipe', 'corrida', 'cpf', 'sexo', 'tamanho_camisa', 'categoria')
    search_fields = ('nome', 'equipe','categoria','sexo')
    list_filter = ('corrida', 'sexo', 'categoria')

@admin.register(ArquivoExcel)
class ArquivoExcelAdmin(admin.ModelAdmin):
    list_display = ('nome', 'data_corrida','criado_em')
    inlines = [CorredorInline]
                                                                                        

