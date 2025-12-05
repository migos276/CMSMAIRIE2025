"""
Modèles pour la gestion du contenu.
"""
from django.db import models
from django.conf import settings
from django.utils.text import slugify


class Categorie(models.Model):
    """Catégorie d'articles."""
    nom = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    icone = models.CharField(max_length=50, blank=True, help_text="Classe CSS de l'icône")
    
    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nom)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.nom


class Article(models.Model):
    """Article ou actualité."""
    titre = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    resume = models.TextField(max_length=500, verbose_name="Résumé")
    contenu = models.TextField()
    image = models.ImageField(upload_to='articles/', blank=True, null=True)
    
    categorie = models.ForeignKey(Categorie, on_delete=models.SET_NULL, null=True, blank=True)
    auteur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    
    publie = models.BooleanField(default=False)
    mis_en_avant = models.BooleanField(default=False, verbose_name="Mis en avant")
    
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    date_publication = models.DateTimeField(null=True, blank=True)
    
    vues = models.PositiveIntegerField(default=0)
    
    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"
        ordering = ['-date_publication', '-date_creation']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titre)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.titre


class Evenement(models.Model):
    """Événement public ou culturel."""
    titre = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    image = models.ImageField(upload_to='evenements/', blank=True, null=True)
    
    lieu = models.CharField(max_length=200)
    adresse = models.TextField(blank=True)
    
    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField(null=True, blank=True)
    
    organisateur = models.CharField(max_length=200, blank=True)
    contact = models.CharField(max_length=200, blank=True)
    
    publie = models.BooleanField(default=False)
    gratuit = models.BooleanField(default=True)
    prix = models.CharField(max_length=100, blank=True)
    
    date_creation = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Événement"
        verbose_name_plural = "Événements"
        ordering = ['date_debut']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titre)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.titre


class Document(models.Model):
    """Document téléchargeable (délibérations, budgets, formulaires)."""
    
    TYPE_CHOICES = [
        ('deliberation', 'Délibération'),
        ('arrete', 'Arrêté'),
        ('budget', 'Document budgétaire'),
        ('formulaire', 'Formulaire'),
        ('rapport', 'Rapport'),
        ('autre', 'Autre'),
    ]
    
    titre = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    fichier = models.FileField(upload_to='documents/')
    type_document = models.CharField(max_length=20, choices=TYPE_CHOICES, default='autre')
    
    numero_reference = models.CharField(max_length=100, blank=True)
    date_document = models.DateField(null=True, blank=True)
    
    public = models.BooleanField(default=True, verbose_name="Accessible au public")
    telechargements = models.PositiveIntegerField(default=0)
    
    date_ajout = models.DateTimeField(auto_now_add=True)
    ajoute_par = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='documents_contenu',
        verbose_name="Ajouté par"
    )
    
    class Meta:
        verbose_name = "Document"
        verbose_name_plural = "Documents"
        ordering = ['-date_ajout']
    
    def __str__(self):
        return self.titre
    
    @property
    def extension(self):
        return self.fichier.name.split('.')[-1].upper() if self.fichier else ''


class ProjetMunicipal(models.Model):
    """Projet municipal avec suivi d'avancement."""
    
    STATUT_CHOICES = [
        ('planifie', 'Planifié'),
        ('en_cours', 'En cours'),
        ('suspendu', 'Suspendu'),
        ('termine', 'Terminé'),
        ('annule', 'Annulé'),
    ]
    
    titre = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    image = models.ImageField(upload_to='projets/', blank=True, null=True)
    
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='planifie')
    pourcentage_avancement = models.PositiveIntegerField(default=0)
    
    budget_alloue = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    budget_execute = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    
    date_debut = models.DateField(null=True, blank=True)
    date_fin_prevue = models.DateField(null=True, blank=True)
    date_fin_reelle = models.DateField(null=True, blank=True)
    
    responsable = models.CharField(max_length=200, blank=True)
    
    publie = models.BooleanField(default=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Projet municipal"
        verbose_name_plural = "Projets municipaux"
        ordering = ['-date_creation']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titre)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.titre
    
    @property
    def taux_execution_budget(self):
        if self.budget_alloue and self.budget_execute:
            return round((self.budget_execute / self.budget_alloue) * 100, 1)
        return 0
