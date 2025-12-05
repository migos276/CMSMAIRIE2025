from django.contrib import admin
from django_tenants.admin import TenantAdminMixin
from .models import Mairie, Domaine


@admin.register(Mairie)
class MairieAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ['nom', 'code', 'region', 'departement', 'actif', 'date_creation']
    list_filter = ['region', 'actif']
    search_fields = ['nom', 'code', 'region', 'departement']
    readonly_fields = ['date_creation']


@admin.register(Domaine)
class DomaineAdmin(admin.ModelAdmin):
    list_display = ['domain', 'tenant', 'is_primary']
    list_filter = ['is_primary']
