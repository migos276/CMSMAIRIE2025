from django.contrib import admin
from .models import Configuration, PageStatique


@admin.register(Configuration)
class ConfigurationAdmin(admin.ModelAdmin):
    list_display = ['cle', 'valeur', 'description']
    search_fields = ['cle', 'description']


@admin.register(PageStatique)
class PageStatiqueAdmin(admin.ModelAdmin):
    list_display = ['titre', 'slug', 'publie', 'ordre', 'date_modification']
    list_filter = ['publie']
    search_fields = ['titre', 'contenu']
    prepopulated_fields = {'slug': ('titre',)}
