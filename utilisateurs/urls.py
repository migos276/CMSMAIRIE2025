from django.urls import path
from . import views

app_name = 'utilisateurs'

urlpatterns = [
    path('connexion/', views.connexion_view, name='connexion'),
    path('deconnexion/', views.deconnexion_view, name='deconnexion'),
    path('inscription/', views.inscription_view, name='inscription'),
    path('profil/', views.profil_view, name='profil'),
]
