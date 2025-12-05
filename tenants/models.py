"""
Modèles de multi-tenancy pour les mairies.
Chaque mairie = un schéma PostgreSQL distinct.
"""
from django.db import models
from django_tenants.models import TenantMixin, DomainMixin


class Mairie(TenantMixin):
    """
    Représente une mairie camerounaise.
    Chaque mairie a son propre schéma de base de données.
    """
    nom = models.CharField(max_length=200, verbose_name="Nom de la mairie")
    code = models.CharField(max_length=50, unique=True, verbose_name="Code unique")
    region = models.CharField(max_length=100, verbose_name="Région")
    departement = models.CharField(max_length=100, verbose_name="Département")
    arrondissement = models.CharField(max_length=100, verbose_name="Arrondissement")
    
    # Informations de contact
    adresse = models.TextField(verbose_name="Adresse physique")
    telephone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    
    # Personnalisation visuelle
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    couleur_primaire = models.CharField(max_length=7, default='#1E40AF', verbose_name="Couleur primaire")
    couleur_secondaire = models.CharField(max_length=7, default='#059669', verbose_name="Couleur secondaire")
    
    # Métadonnées
    date_creation = models.DateTimeField(auto_now_add=True)
    actif = models.BooleanField(default=True)
    
    # Champ requis pour django-tenants
    auto_create_schema = True

    class Meta:
        verbose_name = "Mairie"
        verbose_name_plural = "Mairies"

    def __str__(self):
        return self.nom


class Domaine(DomainMixin):
    """
    Domaines associés à chaque mairie.
    Ex: mairie-yaounde2.arited.cm
    """
    class Meta:
        verbose_name = "Domaine"
        verbose_name_plural = "Domaines"
