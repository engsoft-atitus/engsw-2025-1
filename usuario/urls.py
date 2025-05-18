from django.urls import path
from . import views

urlpatterns = [
    path('cadastro/', views.cadastro_view, name='cadastro'),
    path('login/',views.login_view,name='login'),
    path('xina/',views.xina,name='xina'),#apagar
    path('logout/',views.logout_view,name='logout')
]
