from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import ParticipanteViewSet


urlpatterns = [
    path('', views.index, name='index'),

    # Corridas
    path('corridas/', views.listar_corridas, name='listar_corridas'),
    path('corridas/<int:corrida_id>/inscrever/', views.inscrever_corrida, name='inscrever_corrida'),
    path('resultado_geral', views.resultado_geral, name='resultado_geral'),

    # API RESTful para Participantes
    path('classificacao/', views.classificacao_view, name='classificacao'),

    path('arquivo/<int:pk>/', views.arquivo_detail, name='arquivo_detail'),
    path('arquivo_list/', views.ArquivoExcelListView, name='arquivo_list'),

    
    path('register/', views.register_view, name="register"),
    path('teste_login/', views.teste_login, name='teste_login'),
    path('cadastro/', views.cadastro, name='cadastro'),
  
    path('logout/', views.logout_confirm, name='logout_confirm'),  # página de confirmação
    path('logout/confirm/', views.logout_view, name='logout'),     # ação real de logout


]                                                                               

