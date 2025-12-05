"""
Modèles de base pour le CMS.
"""
from django.db import models


class Configuration(models.Model):
    """Configuration spécifique à chaque mairie."""
    cle = models.CharField(max_length=100, unique=True)
    valeur = models.TextField()
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name = "Configuration"
        verbose_name_plural = "Configurations"
    
    def __str__(self):
        return self.cle


class PageStatique(models.Model):
    """Pages statiques du site (À propos, Mentions légales, etc.)"""
    titre = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    contenu = models.TextField()
    meta_description = models.CharField(max_length=300, blank=True)
    publie = models.BooleanField(default=True)
    ordre = models.IntegerField(default=0)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Page statique"
        verbose_name_plural = "Pages statiques"
        ordering = ['ordre', 'titre']
    
    def __str__(self):
        return self.titre
