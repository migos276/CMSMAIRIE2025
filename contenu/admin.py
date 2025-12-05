from django.contrib import admin
from .models import Categorie, Article, Evenement, Document, ProjetMunicipal


@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ['nom', 'slug']
    prepopulated_fields = {'slug': ('nom',)}


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['titre', 'categorie', 'auteur', 'publie', 'mis_en_avant', 'date_publication', 'vues']
    list_filter = ['publie', 'mis_en_avant', 'categorie', 'date_publication']
    search_fields = ['titre', 'contenu']
    prepopulated_fields = {'slug': ('titre',)}
    date_hierarchy = 'date_creation'


@admin.register(Evenement)
class EvenementAdmin(admin.ModelAdmin):
    list_display = ['titre', 'lieu', 'date_debut', 'date_fin', 'publie', 'gratuit']
    list_filter = ['publie', 'gratuit', 'date_debut']
    search_fields = ['titre', 'description', 'lieu']
    prepopulated_fields = {'slug': ('titre',)}


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['titre', 'type_document', 'public', 'date_ajout', 'telechargements']
    list_filter = ['type_document', 'public', 'date_ajout']
    search_fields = ['titre', 'description', 'numero_reference']


@admin.register(ProjetMunicipal)
class ProjetMunicipalAdmin(admin.ModelAdmin):
    list_display = ['titre', 'statut', 'pourcentage_avancement', 'budget_alloue', 'publie']
    list_filter = ['statut', 'publie']
    search_fields = ['titre', 'description']
    prepopulated_fields = {'slug': ('titre',)}
