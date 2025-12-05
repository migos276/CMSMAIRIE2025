"""
Vues pour les services en ligne.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import ListView, CreateView, DetailView, TemplateView
from django.http import JsonResponse
from datetime import datetime, timedelta
from .models import (
    TypeRendezVous, CreneauDisponible, RendezVous,
    CategorieReclamation, Reclamation, InscriptionNewsletter
)
from .forms import RendezVousForm, ReclamationForm, NewsletterForm


class AccueilServicesView(TemplateView):
    """Page d'accueil des services."""
    template_name = 'services/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['types_rdv'] = TypeRendezVous.objects.filter(actif=True)
        context['categories_reclamation'] = CategorieReclamation.objects.all()
        return context


class PrendreRendezVousView(CreateView):
    """Vue pour prendre un rendez-vous."""
    model = RendezVous
    form_class = RendezVousForm
    template_name = 'services/prendre_rdv.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['types_rdv'] = TypeRendezVous.objects.filter(actif=True)
        return context
    
    def form_valid(self, form):
        rdv = form.save(commit=False)
        if self.request.user.is_authenticated:
            rdv.citoyen = self.request.user
        rdv.save()
        messages.success(
            self.request,
            f"Votre rendez-vous a été confirmé. Numéro : {rdv.numero}"
        )
        return redirect('services:confirmation_rdv', numero=rdv.numero)


def confirmation_rdv_view(request, numero):
    """Confirmation du rendez-vous."""
    rdv = get_object_or_404(RendezVous, numero=numero)
    return render(request, 'services/confirmation_rdv.html', {'rdv': rdv})


def creneaux_disponibles_api(request):
    """API pour récupérer les créneaux disponibles."""
    type_rdv_id = request.GET.get('type_rdv')
    date_str = request.GET.get('date')
    
    if not type_rdv_id or not date_str:
        return JsonResponse({'creneaux': []})
    
    try:
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        jour_semaine = date.weekday()
        
        creneaux = CreneauDisponible.objects.filter(
            type_rdv_id=type_rdv_id,
            jour=jour_semaine
        )
        
        # Vérifier les places disponibles
        creneaux_dispo = []
        for creneau in creneaux:
            rdv_existants = RendezVous.objects.filter(
                type_rdv_id=type_rdv_id,
                date=date,
                heure=creneau.heure_debut,
                statut='confirme'
            ).count()
            
            if rdv_existants < creneau.places_max:
                creneaux_dispo.append({
                    'heure': creneau.heure_debut.strftime('%H:%M'),
                    'places_restantes': creneau.places_max - rdv_existants
                })
        
        return JsonResponse({'creneaux': creneaux_dispo})
    
    except (ValueError, TypeError):
        return JsonResponse({'creneaux': []})


class SoumettreReclamationView(CreateView):
    """Vue pour soumettre une réclamation."""
    model = Reclamation
    form_class = ReclamationForm
    template_name = 'services/soumettre_reclamation.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = CategorieReclamation.objects.all()
        return context
    
    def form_valid(self, form):
        reclamation = form.save(commit=False)
        if self.request.user.is_authenticated:
            reclamation.auteur = self.request.user
        reclamation.save()
        messages.success(
            self.request,
            f"Votre réclamation a été enregistrée. Numéro de suivi : {reclamation.numero}"
        )
        return redirect('services:suivi_reclamation', numero=reclamation.numero)


def suivi_reclamation_view(request, numero=None):
    """Suivi d'une réclamation."""
    reclamation = None
    
    if numero:
        try:
            reclamation = Reclamation.objects.get(numero=numero)
        except Reclamation.DoesNotExist:
            messages.error(request, "Réclamation non trouvée.")
    
    elif request.method == 'POST':
        numero_input = request.POST.get('numero', '').strip()
        if numero_input:
            return redirect('services:suivi_reclamation', numero=numero_input)
    
    return render(request, 'services/suivi_reclamation.html', {
        'reclamation': reclamation,
        'numero': numero
    })


def inscription_newsletter_view(request):
    """Inscription à la newsletter."""
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Vous êtes inscrit à la newsletter !")
            return redirect('core:accueil')
    else:
        form = NewsletterForm()
    
    return render(request, 'services/newsletter.html', {'form': form})


class MesRendezVousView(ListView):
    """Liste des rendez-vous de l'utilisateur connecté."""
    model = RendezVous
    template_name = 'services/mes_rdv.html'
    context_object_name = 'rendez_vous'
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return RendezVous.objects.filter(citoyen=self.request.user)
        return RendezVous.objects.none()


class MesReclamationsView(ListView):
    """Liste des réclamations de l'utilisateur connecté."""
    model = Reclamation
    template_name = 'services/mes_reclamations.html'
    context_object_name = 'reclamations'
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Reclamation.objects.filter(auteur=self.request.user)
        return Reclamation.objects.none()
