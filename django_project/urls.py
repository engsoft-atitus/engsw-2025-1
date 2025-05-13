"""
URL configuration for django_structure project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from musica import views
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('usuario/', include('usuario.urls')), #TODO antes era '' vazio, CORRIGIR
    path('', views.buscar_musicas, name='buscar_musicas'),
    path('player/', views.player, name='player'),
    path('salvar/', views.salvar_musica, name='salvar_musica'),
    path('playlists/', views.listar_playlists, name='listar_playlists'),
    path('playlist/<int:playlist_id>/', views.ver_playlist, name='ver_playlist'),
    path('criar_playlist/', views.criar_playlist, name='criar_playlist'),
    path("comunidade/",include("comunidade.urls"))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
