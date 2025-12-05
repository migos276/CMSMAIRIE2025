"""
Modèles pour la gestion des actes d'état civil.
- Actes de naissance
- Actes de mariage
- Actes de décès
- Livrets de famille
"""
from django.db import models
from django.conf import settings
import uuid


class ActeBase(models.Model):
    """Modèle de base pour tous les actes d'état civil."""
    
    STATUT_CHOICES = [
        ('en_attente', 'En attente de traitement'),
        ('en_cours', 'En cours de traitement'),
        ('valide', 'Validé'),
        ('rejete', 'Rejeté'),
        ('pret', 'Prêt pour retrait'),
        ('delivre', 'Délivré'),
    ]
    
    numero_reference = models.CharField(max_length=50, unique=True, editable=False)
    numero_suivi = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
    
    # Demandeur
    demandeur = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='%(class)s_demandes'
    )
    demandeur_nom = models.CharField(max_length=100)
    demandeur_prenom = models.CharField(max_length=100)
    demandeur_telephone = models.CharField(max_length=20)
    demandeur_email = models.EmailField(blank=True)
    
    # Traitement
    agent_traitant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='%(class)s_traites'
    )
    commentaire_agent = models.TextField(blank=True)
    motif_rejet = models.TextField(blank=True)
    
    # Dates
    date_demande = models.DateTimeField(auto_now_add=True)
    date_traitement = models.DateTimeField(null=True, blank=True)
    date_delivrance = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        abstract = True
        ordering = ['-date_demande']
    
    def save(self, *args, **kwargs):
        if not self.numero_reference:
            prefix = self.get_prefix()
            from django.utils import timezone
            year = timezone.now().year
            count = self.__class__.objects.filter(date_demande__year=year).count() + 1
            self.numero_reference = f"{prefix}-{year}-{count:05d}"
        super().save(*args, **kwargs)
    
    def get_prefix(self):
        return "ACT"


class ActeNaissance(ActeBase):
    """Demande d'acte de naissance."""
    
    TYPE_CHOICES = [
        ('copie_integrale', 'Copie intégrale'),
        ('extrait', 'Extrait'),
        ('extrait_plurilingue', 'Extrait plurilingue'),
    ]
    
    type_acte = models.CharField(max_length=30, choices=TYPE_CHOICES, default='extrait')
    
    # Informations sur la personne concernée
    nom_concerne = models.CharField(max_length=100, verbose_name="Nom")
    prenom_concerne = models.CharField(max_length=100, verbose_name="Prénom(s)")
    date_naissance = models.DateField(verbose_name="Date de naissance")
    lieu_naissance = models.CharField(max_length=200, verbose_name="Lieu de naissance")
    
    # Parents
    nom_pere = models.CharField(max_length=100, verbose_name="Nom du père")
    prenom_pere = models.CharField(max_length=100, verbose_name="Prénom(s) du père")
    nom_mere = models.CharField(max_length=100, verbose_name="Nom de la mère")
    prenom_mere = models.CharField(max_length=100, verbose_name="Prénom(s) de la mère")
    
    # Numéro d'acte original (si connu)
    numero_acte_original = models.CharField(max_length=50, blank=True)
    annee_enregistrement = models.IntegerField(null=True, blank=True)
    
    # Pièces justificatives
    piece_identite = models.FileField(upload_to='actes/naissance/pi/', blank=True, null=True)
    
    class Meta:
        verbose_name = "Acte de naissance"
        verbose_name_plural = "Actes de naissance"
    
    def get_prefix(self):
        return "NAIS"
    
    def __str__(self):
        return f"Acte naissance - {self.prenom_concerne} {self.nom_concerne} ({self.numero_reference})"


class ActeMariage(ActeBase):
    """Demande d'acte de mariage."""
    
    TYPE_CHOICES = [
        ('copie_integrale', 'Copie intégrale'),
        ('extrait', 'Extrait'),
    ]
    
    type_acte = models.CharField(max_length=30, choices=TYPE_CHOICES, default='extrait')
    
    # Époux
    nom_epoux = models.CharField(max_length=100)
    prenom_epoux = models.CharField(max_length=100)
    date_naissance_epoux = models.DateField()
    
    # Épouse
    nom_epouse = models.CharField(max_length=100)
    prenom_epouse = models.CharField(max_length=100)
    date_naissance_epouse = models.DateField()
    
    # Mariage
    date_mariage = models.DateField()
    lieu_mariage = models.CharField(max_length=200)
    
    # Numéro d'acte original
    numero_acte_original = models.CharField(max_length=50, blank=True)
    
    class Meta:
        verbose_name = "Acte de mariage"
        verbose_name_plural = "Actes de mariage"
    
    def get_prefix(self):
        return "MAR"
    
    def __str__(self):
        return f"Acte mariage - {self.prenom_epoux} {self.nom_epoux} & {self.prenom_epouse} {self.nom_epouse}"


class ActeDeces(ActeBase):
    """Demande d'acte de décès."""
    
    TYPE_CHOICES = [
        ('copie_integrale', 'Copie intégrale'),
        ('extrait', 'Extrait'),
    ]
    
    type_acte = models.CharField(max_length=30, choices=TYPE_CHOICES, default='extrait')
    
    # Défunt
    nom_defunt = models.CharField(max_length=100)
    prenom_defunt = models.CharField(max_length=100)
    date_naissance_defunt = models.DateField()
    date_deces = models.DateField()
    lieu_deces = models.CharField(max_length=200)
    
    # Lien avec le demandeur
    lien_demandeur = models.CharField(max_length=100, verbose_name="Lien avec le défunt")
    
    # Numéro d'acte original
    numero_acte_original = models.CharField(max_length=50, blank=True)
    
    class Meta:
        verbose_name = "Acte de décès"
        verbose_name_plural = "Actes de décès"
    
    def get_prefix(self):
        return "DEC"
    
    def __str__(self):
        return f"Acte décès - {self.prenom_defunt} {self.nom_defunt}"


class LivretFamille(ActeBase):
    """Demande de livret de famille."""
    
    MOTIF_CHOICES = [
        ('premiere_demande', 'Première demande'),
        ('duplicata', 'Duplicata'),
        ('mise_a_jour', 'Mise à jour'),
    ]
    
    motif = models.CharField(max_length=20, choices=MOTIF_CHOICES, default='premiere_demande')
    
    # Chef de famille
    nom_chef = models.CharField(max_length=100)
    prenom_chef = models.CharField(max_length=100)
    date_naissance_chef = models.DateField()
    
    # Conjoint
    nom_conjoint = models.CharField(max_length=100, blank=True)
    prenom_conjoint = models.CharField(max_length=100, blank=True)
    date_naissance_conjoint = models.DateField(null=True, blank=True)
    
    # Mariage
    date_mariage = models.DateField(null=True, blank=True)
    lieu_mariage = models.CharField(max_length=200, blank=True)
    
    # Nombre d'enfants
    nombre_enfants = models.IntegerField(default=0)
    
    class Meta:
        verbose_name = "Livret de famille"
        verbose_name_plural = "Livrets de famille"
    
    def get_prefix(self):
        return "LIV"
    
    def __str__(self):
        return f"Livret famille - {self.prenom_chef} {self.nom_chef}"
