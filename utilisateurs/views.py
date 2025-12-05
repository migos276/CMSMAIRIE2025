"""
Vues pour l'authentification et la gestion des utilisateurs.
"""
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import CreateView, UpdateView
from .models import Utilisateur
from .forms import InscriptionForm, ConnexionForm, ProfilForm


def connexion_view(request):
    """Vue de connexion."""
    if request.user.is_authenticated:
        return redirect('core:tableau_de_bord')
    
    if request.method == 'POST':
        form = ConnexionForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Bienvenue, {user.get_full_name()} !")
                return redirect('core:tableau_de_bord')
            else:
                messages.error(request, "Email ou mot de passe incorrect.")
    else:
        form = ConnexionForm()
    
    return render(request, 'utilisateurs/connexion.html', {'form': form})


def deconnexion_view(request):
    """Vue de déconnexion."""
    logout(request)
    messages.info(request, "Vous avez été déconnecté.")
    return redirect('core:accueil')


def inscription_view(request):
    """Vue d'inscription pour les citoyens."""
    if request.user.is_authenticated:
        return redirect('core:accueil')
    
    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'citoyen'
            user.save()
            login(request, user)
            messages.success(request, "Votre compte a été créé avec succès !")
            return redirect('core:accueil')
    else:
        form = InscriptionForm()
    
    return render(request, 'utilisateurs/inscription.html', {'form': form})


@login_required
def profil_view(request):
    """Vue du profil utilisateur."""
    if request.method == 'POST':
        form = ProfilForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil mis à jour avec succès !")
            return redirect('utilisateurs:profil')
    else:
        form = ProfilForm(instance=request.user)
    
    return render(request, 'utilisateurs/profil.html', {'form': form})
