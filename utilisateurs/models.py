"""
Modèles utilisateurs avec rôles granulaires.
"""
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UtilisateurManager(BaseUserManager):
    """Manager personnalisé pour les utilisateurs."""
    
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("L'email est obligatoire")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'super_admin')
        return self.create_user(email, password, **extra_fields)


class Utilisateur(AbstractUser):
    """
    Utilisateur personnalisé avec rôles.
    Rôles:
    - super_admin: ARITED (accès toutes mairies)
    - admin_mairie: Administrateur de la mairie
    - agent_etat_civil: Agent état civil
    - agent_urbanisme: Agent urbanisme
    - agent_communication: Agent communication
    - citoyen: Citoyen (compte public)
    """
    ROLE_CHOICES = [
        ('super_admin', 'Super Administrateur ARITED'),
        ('admin_mairie', 'Administrateur Mairie'),
        ('agent_etat_civil', 'Agent État Civil'),
        ('agent_urbanisme', 'Agent Urbanisme'),
        ('agent_communication', 'Agent Communication'),
        ('citoyen', 'Citoyen'),
    ]
    
    username = None
    email = models.EmailField(unique=True, verbose_name="Adresse email")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='citoyen')
    
    # Informations personnelles
    telephone = models.CharField(max_length=20, blank=True)
    adresse = models.TextField(blank=True)
    cni = models.CharField(max_length=50, blank=True, verbose_name="Numéro CNI")
    
    # Dates
    date_inscription = models.DateTimeField(auto_now_add=True)
    derniere_connexion = models.DateTimeField(null=True, blank=True)
    
    objects = UtilisateurManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display()})"
    
    def is_admin(self):
        return self.role in ['super_admin', 'admin_mairie']
    
    def is_agent(self):
        return self.role in ['agent_etat_civil', 'agent_urbanisme', 'agent_communication']
    
    def can_manage_etat_civil(self):
        return self.role in ['super_admin', 'admin_mairie', 'agent_etat_civil']
    
    def can_manage_contenu(self):
        return self.role in ['super_admin', 'admin_mairie', 'agent_communication']
    
    def can_manage_urbanisme(self):
        return self.role in ['super_admin', 'admin_mairie', 'agent_urbanisme']
