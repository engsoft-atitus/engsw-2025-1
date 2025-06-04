from django.urls import path
from . import views

urlpatterns = [
    path('cadastro/', views.cadastro_view, name='cadastro'),
    path('login/' , views.login_view, name='login'),
    path('perfil/<str:username>/', views.perfil_view, name='perfil'),
    path('genero/', views.genero_view, name='genero'),
    path('logout/', views.logout_view, name='logout'),
    path('principal/', views.principal_view, name='principal'),
    path('buscar-usuario/', views.buscar_usuario_view, name='buscar-usuario'),
]
