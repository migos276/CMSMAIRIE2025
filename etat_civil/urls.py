from django.urls import path
from . import views

app_name = 'etat_civil'

urlpatterns = [
    # Accueil État Civil
    path('', views.AccueilEtatCivilView.as_view(), name='accueil'),
    
    # Demandes publiques
    path('naissance/', views.DemandeActeNaissanceView.as_view(), name='demande_naissance'),
    path('mariage/', views.DemandeActeMariageView.as_view(), name='demande_mariage'),
    path('deces/', views.DemandeActeDecesView.as_view(), name='demande_deces'),
    path('livret-famille/', views.DemandeLivretFamilleView.as_view(), name='demande_livret'),
    
    # Suivi
    path('suivi/', views.suivi_demande_view, name='suivi_form'),
    path('suivi/<uuid:numero_suivi>/', views.suivi_demande_view, name='suivi'),
    
    # Gestion agents
    path('agent/demandes/', views.liste_demandes_view, name='liste_demandes'),
    path('agent/traiter/<str:type_acte>/<int:pk>/', views.traiter_demande_view, name='traiter_demande'),
]
