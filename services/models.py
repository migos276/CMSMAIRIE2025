"""
Modèles pour les services en ligne.
"""
from django.db import models
from django.conf import settings
import uuid


class TypeRendezVous(models.Model):
    """Types de rendez-vous disponibles."""
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    duree_minutes = models.PositiveIntegerField(default=30)
    service = models.CharField(max_length=100, help_text="Service concerné (état civil, urbanisme, etc.)")
    actif = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Type de rendez-vous"
        verbose_name_plural = "Types de rendez-vous"
    
    def __str__(self):
        return self.nom


class CreneauDisponible(models.Model):
    """Créneaux disponibles pour les rendez-vous."""
    JOUR_CHOICES = [
        (0, 'Lundi'),
        (1, 'Mardi'),
        (2, 'Mercredi'),
        (3, 'Jeudi'),
        (4, 'Vendredi'),
        (5, 'Samedi'),
    ]
    
    type_rdv = models.ForeignKey(TypeRendezVous, on_delete=models.CASCADE, related_name='creneaux')
    jour = models.IntegerField(choices=JOUR_CHOICES)
    heure_debut = models.TimeField()
    heure_fin = models.TimeField()
    places_max = models.PositiveIntegerField(default=1)
    
    class Meta:
        verbose_name = "Créneau disponible"
        verbose_name_plural = "Créneaux disponibles"
        ordering = ['jour', 'heure_debut']
    
    def __str__(self):
        return f"{self.get_jour_display()} {self.heure_debut}-{self.heure_fin}"


class RendezVous(models.Model):
    """Rendez-vous pris par les citoyens."""
    
    STATUT_CHOICES = [
        ('confirme', 'Confirmé'),
        ('annule', 'Annulé'),
        ('termine', 'Terminé'),
        ('absent', 'Absent'),
    ]
    
    numero = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    type_rdv = models.ForeignKey(TypeRendezVous, on_delete=models.CASCADE)
    
    # Demandeur
    citoyen = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    
    # Rendez-vous
    date = models.DateField()
    heure = models.TimeField()
    motif = models.TextField(blank=True)
    
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='confirme')
    notes_agent = models.TextField(blank=True)
    
    date_creation = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Rendez-vous"
        verbose_name_plural = "Rendez-vous"
        ordering = ['date', 'heure']
    
    def __str__(self):
        return f"RDV {self.numero} - {self.prenom} {self.nom} le {self.date}"


class CategorieReclamation(models.Model):
    """Catégories de réclamations."""
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icone = models.CharField(max_length=50, blank=True)
    
    class Meta:
        verbose_name = "Catégorie de réclamation"
        verbose_name_plural = "Catégories de réclamations"
    
    def __str__(self):
        return self.nom


class Reclamation(models.Model):
    """Réclamation citoyenne."""
    
    STATUT_CHOICES = [
        ('soumise', 'Soumise'),
        ('en_cours', 'En cours de traitement'),
        ('resolue', 'Résolue'),
        ('fermee', 'Fermée'),
    ]
    
    PRIORITE_CHOICES = [
        ('basse', 'Basse'),
        ('normale', 'Normale'),
        ('haute', 'Haute'),
        ('urgente', 'Urgente'),
    ]
    
    numero = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    categorie = models.ForeignKey(CategorieReclamation, on_delete=models.SET_NULL, null=True)
    
    # Auteur
    auteur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    
    # Réclamation
    titre = models.CharField(max_length=200)
    description = models.TextField()
    localisation = models.CharField(max_length=300, blank=True, help_text="Adresse ou quartier concerné")
    photo = models.ImageField(upload_to='reclamations/', blank=True, null=True)
    
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='soumise')
    priorite = models.CharField(max_length=20, choices=PRIORITE_CHOICES, default='normale')
    
    # Traitement
    agent_traitant = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='reclamations_traitees'
    )
    reponse = models.TextField(blank=True)
    
    date_creation = models.DateTimeField(auto_now_add=True)
    date_traitement = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Réclamation"
        verbose_name_plural = "Réclamations"
        ordering = ['-date_creation']
    
    def __str__(self):
        return f"{self.numero} - {self.titre}"


class DemandeActe(models.Model):
    """Modèle unifié pour le suivi des demandes d'actes (vue simplifiée)."""
    
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('en_cours', 'En cours'),
        ('valide', 'Validé'),
        ('rejete', 'Rejeté'),
        ('pret', 'Prêt'),
        ('delivre', 'Délivré'),
    ]
    
    numero_suivi = models.UUIDField(default=uuid.uuid4, editable=False)
    type_acte = models.CharField(max_length=50)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
    date_demande = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Demande d'acte"
        verbose_name_plural = "Demandes d'actes"


class InscriptionNewsletter(models.Model):
    """Inscription à la newsletter municipale."""
    email = models.EmailField(unique=True)
    nom = models.CharField(max_length=100, blank=True)
    prenom = models.CharField(max_length=100, blank=True)
    actif = models.BooleanField(default=True)
    date_inscription = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Inscription newsletter"
        verbose_name_plural = "Inscriptions newsletter"
    
    def __str__(self):
        return self.email
