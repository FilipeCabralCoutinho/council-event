from django.urls import path
from . import views

app_name = 'plenary_control'

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('api/participantes/', views.get_participantes, name='api_participantes'),
    path('api/buscar/', views.buscar_participantes, name='api_buscar'),
    path('api/atualizar-plenario/', views.atualizar_plenario, name='api_atualizar_plenario'),
]