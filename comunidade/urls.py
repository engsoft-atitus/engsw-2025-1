from django.urls import path
from comunidade import views

urlpatterns = [
    # path (url da view, nome da função)
    path('',views.index,name='base'),
    path('community_create/',views.community_create,name='community_create'),
    path('<str:nome_tag>/',views.community_view,name='community'),
    path('<str:nome_tag>/edit',views.community_edit,name="community_edit"),
    path('<str:nome_tag>/delete',views.community_delete,name="community_delete")
] 