"""
Formulaires pour les services en ligne.
"""
from django import forms
from .models import RendezVous, Reclamation, InscriptionNewsletter


class RendezVousForm(forms.ModelForm):
    """Formulaire de prise de rendez-vous."""
    
    class Meta:
        model = RendezVous
        fields = ['type_rdv', 'nom', 'prenom', 'telephone', 'email', 'date', 'heure', 'motif']
        widgets = {
            'type_rdv': forms.Select(attrs={'class': 'w-full px-4 py-2 border rounded-lg'}),
            'nom': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg'}),
            'prenom': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg'}),
            'telephone': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg'}),
            'email': forms.EmailInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'w-full px-4 py-2 border rounded-lg'}),
            'heure': forms.TimeInput(attrs={'type': 'time', 'class': 'w-full px-4 py-2 border rounded-lg'}),
            'motif': forms.Textarea(attrs={'class': 'w-full px-4 py-2 border rounded-lg', 'rows': 3}),
        }


class ReclamationForm(forms.ModelForm):
    """Formulaire de réclamation."""
    
    class Meta:
        model = Reclamation
        fields = ['categorie', 'nom', 'prenom', 'telephone', 'email', 'titre', 'description', 'localisation', 'photo']
        widgets = {
            'categorie': forms.Select(attrs={'class': 'w-full px-4 py-2 border rounded-lg'}),
            'nom': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg'}),
            'prenom': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg'}),
            'telephone': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg'}),
            'email': forms.EmailInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg'}),
            'titre': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg'}),
            'description': forms.Textarea(attrs={'class': 'w-full px-4 py-2 border rounded-lg', 'rows': 5}),
            'localisation': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg'}),
            'photo': forms.FileInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg'}),
        }


class NewsletterForm(forms.ModelForm):
    """Formulaire d'inscription à la newsletter."""
    
    class Meta:
        model = InscriptionNewsletter
        fields = ['email', 'nom', 'prenom']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg', 'placeholder': 'votre@email.com'}),
            'nom': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg'}),
            'prenom': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg'}),
        }
