from django.contrib import admin
from .models import (
    TypeRendezVous, CreneauDisponible, RendezVous,
    CategorieReclamation, Reclamation, InscriptionNewsletter
)


@admin.register(TypeRendezVous)
class TypeRendezVousAdmin(admin.ModelAdmin):
    list_display = ['nom', 'service', 'duree_minutes', 'actif']
    list_filter = ['actif', 'service']


@admin.register(CreneauDisponible)
class CreneauDisponibleAdmin(admin.ModelAdmin):
    list_display = ['type_rdv', 'jour', 'heure_debut', 'heure_fin', 'places_max']
    list_filter = ['type_rdv', 'jour']


@admin.register(RendezVous)
class RendezVousAdmin(admin.ModelAdmin):
    list_display = ['numero', 'type_rdv', 'nom', 'prenom', 'date', 'heure', 'statut']
    list_filter = ['statut', 'type_rdv', 'date']
    search_fields = ['numero', 'nom', 'prenom', 'telephone']
    date_hierarchy = 'date'


@admin.register(CategorieReclamation)
class CategorieReclamationAdmin(admin.ModelAdmin):
    list_display = ['nom', 'description']


@admin.register(Reclamation)
class ReclamationAdmin(admin.ModelAdmin):
    list_display = ['numero', 'titre', 'categorie', 'statut', 'priorite', 'date_creation']
    list_filter = ['statut', 'priorite', 'categorie']
    search_fields = ['numero', 'titre', 'nom', 'prenom']
    date_hierarchy = 'date_creation'


@admin.register(InscriptionNewsletter)
class InscriptionNewsletterAdmin(admin.ModelAdmin):
    list_display = ['email', 'nom', 'prenom', 'actif', 'date_inscription']
    list_filter = ['actif']
    search_fields = ['email', 'nom', 'prenom']
