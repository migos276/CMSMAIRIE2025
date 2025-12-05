from django.urls import path
from . import views

app_name = 'services'

urlpatterns = [
    # Accueil Services
    path('', views.AccueilServicesView.as_view(), name='index'),
    
    # Rendez-vous
    path('rendez-vous/', views.PrendreRendezVousView.as_view(), name='prendre_rdv'),
    path('rendez-vous/confirmation/<uuid:numero>/', views.confirmation_rdv_view, name='confirmation_rdv'),
    path('rendez-vous/mes-rdv/', views.MesRendezVousView.as_view(), name='mes_rdv'),
    path('api/creneaux/', views.creneaux_disponibles_api, name='api_creneaux'),
    
    # Réclamations
    path('reclamation/', views.SoumettreReclamationView.as_view(), name='soumettre_reclamation'),
    path('reclamation/suivi/', views.suivi_reclamation_view, name='suivi_reclamation_form'),
    path('reclamation/suivi/<uuid:numero>/', views.suivi_reclamation_view, name='suivi_reclamation'),
    path('reclamation/mes-reclamations/', views.MesReclamationsView.as_view(), name='mes_reclamations'),
    
    # Newsletter
    path('newsletter/', views.inscription_newsletter_view, name='newsletter'),
]
