# accounts/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='home'),  # Redirige la raíz al dashboard
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('generar-qr/', views.generar_qr, name='generar_qr'),
    path('seleccionar-lotes/', views.seleccionar_lotes, name='seleccionar_lotes'),
    path('historial-bajas/', views.historial_bajas, name='historial_bajas'),
    path('validar-qr/<str:folio>/', views.validar_qr, name='validar_qr'),
    path('formulario-qr/<str:folio>/', views.formulario_qr, name='formulario_qr'),
]

