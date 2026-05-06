from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),

    # Corridas
    path('corridas/', views.listar_corridas, name='listar_corridas'),
    path('corridas/<int:corrida_id>/inscrever/', views.inscrever_corrida, name='inscrever_corrida'),
    path('eventos/buscar-cpf/', views.buscar_usuario_cpf, name='buscar_usuario_cpf'),

    # Rotas de participantes
    path('classificacao/', views.classificacao_view, name='classificacao'),

    path('arquivo/<int:pk>/', views.arquivo_detail, name='arquivo_detail'),
    path('arquivo_list/', views.ArquivoExcelListView, name='arquivo_list'),

    
    path('register/', views.register_view, name="register"),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('auth/', views.auth_page, name='auth_page'),  # Página unificada login/logout
  
    path('logout/', views.logout_confirm, name='logout_confirm'),  # página de confirmação
    path('logout/confirm/', views.logout_view, name='logout'),     # ação real de logout
    path('logout-rapido/', views.logout_rapido, name='logout_rapido'),  # logout direto via POST

    path('historico_usuario/', views.historico_usuario, name='historico_usuario'),
    path('eventos/buscar-nomes/', views.buscar_nomes_autocomplete, name='buscar_nomes_autocomplete'),

]                                                                               
