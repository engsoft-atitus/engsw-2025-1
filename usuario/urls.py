from django.urls import path
from . import views

urlpatterns = [
    path('cadastro/', views.cadastro_view, name='cadastro'),
    path('login/' , views.login_view, name='login'),
    path('perfil/', views.perfil_view, name='perfil'),
    path('genero/', views.genero_view, name='genero')
]
