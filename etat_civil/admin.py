from django.contrib import admin
from .models import ActeNaissance, ActeMariage, ActeDeces, LivretFamille


class ActeBaseAdmin(admin.ModelAdmin):
    list_display = ['numero_reference', 'demandeur_nom', 'demandeur_prenom', 'statut', 'date_demande']
    list_filter = ['statut', 'date_demande']
    search_fields = ['numero_reference', 'numero_suivi', 'demandeur_nom', 'demandeur_prenom']
    readonly_fields = ['numero_reference', 'numero_suivi', 'date_demande']
    date_hierarchy = 'date_demande'


@admin.register(ActeNaissance)
class ActeNaissanceAdmin(ActeBaseAdmin):
    list_display = ['numero_reference', 'nom_concerne', 'prenom_concerne', 'date_naissance', 'statut', 'date_demande']
    search_fields = ActeBaseAdmin.search_fields + ['nom_concerne', 'prenom_concerne']


@admin.register(ActeMariage)
class ActeMariageAdmin(ActeBaseAdmin):
    list_display = ['numero_reference', 'nom_epoux', 'nom_epouse', 'date_mariage', 'statut', 'date_demande']
    search_fields = ActeBaseAdmin.search_fields + ['nom_epoux', 'nom_epouse']


@admin.register(ActeDeces)
class ActeDecesAdmin(ActeBaseAdmin):
    list_display = ['numero_reference', 'nom_defunt', 'prenom_defunt', 'date_deces', 'statut', 'date_demande']
    search_fields = ActeBaseAdmin.search_fields + ['nom_defunt', 'prenom_defunt']


@admin.register(LivretFamille)
class LivretFamilleAdmin(ActeBaseAdmin):
    list_display = ['numero_reference', 'nom_chef', 'prenom_chef', 'motif', 'statut', 'date_demande']
    search_fields = ActeBaseAdmin.search_fields + ['nom_chef', 'prenom_chef']
