"""
Formulaires pour les utilisateurs.
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Utilisateur


class ConnexionForm(forms.Form):
    """Formulaire de connexion."""
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500',
            'placeholder': 'votre@email.com'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Votre mot de passe'
        })
    )


class InscriptionForm(UserCreationForm):
    """Formulaire d'inscription citoyen."""
    class Meta:
        model = Utilisateur
        fields = ['email', 'first_name', 'last_name', 'telephone', 'cni', 'password1', 'password2']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg'}),
            'first_name': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg'}),
            'last_name': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg'}),
            'telephone': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg'}),
            'cni': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg'}),
        }


class ProfilForm(forms.ModelForm):
    """Formulaire de modification du profil."""
    class Meta:
        model = Utilisateur
        fields = ['first_name', 'last_name', 'telephone', 'adresse', 'cni']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg'}),
            'last_name': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg'}),
            'telephone': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg'}),
            'adresse': forms.Textarea(attrs={'class': 'w-full px-4 py-2 border rounded-lg', 'rows': 3}),
            'cni': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg'}),
        }
