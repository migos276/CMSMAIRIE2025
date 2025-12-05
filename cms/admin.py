"""
Configuration admin Django pour le CMS.
"""
from django.contrib import admin
from .models import (
    ImagePersonnalisee, DocumentPersonnalise,
    MenuPrincipal, MenuItem, Partenaire, ServiceMairie,
    MembreEquipe, FAQ, Temoignage, CategorieArticle
)


# Note: La plupart des modèles CMS sont gérés via Wagtail Admin
# Ces configurations sont pour l'admin Django standard si nécessaire

@admin.register(Partenaire)
class PartenaireAdmin(admin.ModelAdmin):
    list_display = ['nom', 'site_web', 'ordre', 'actif']
    list_filter = ['actif']
    list_editable = ['ordre', 'actif']


@admin.register(ServiceMairie)
class ServiceMairieAdmin(admin.ModelAdmin):
    list_display = ['nom', 'ordre', 'actif']
    list_filter = ['actif']
    list_editable = ['ordre', 'actif']


@admin.register(MembreEquipe)
class MembreEquipeAdmin(admin.ModelAdmin):
    list_display = ['nom', 'fonction', 'ordre', 'actif']
    list_filter = ['actif']
    list_editable = ['ordre', 'actif']


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'categorie', 'ordre', 'publie']
    list_filter = ['categorie', 'publie']
    list_editable = ['ordre', 'publie']


@admin.register(Temoignage)
class TemoignageAdmin(admin.ModelAdmin):
    list_display = ['nom', 'note', 'publie', 'date']
    list_filter = ['publie', 'note']


@admin.register(CategorieArticle)
class CategorieArticleAdmin(admin.ModelAdmin):
    list_display = ['nom', 'slug']
    prepopulated_fields = {'slug': ('nom',)}
