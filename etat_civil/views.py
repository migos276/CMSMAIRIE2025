"""
Vues pour la gestion des actes d'état civil.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from .models import ActeNaissance, ActeMariage, ActeDeces, LivretFamille
from .forms import ActeNaissanceForm, ActeMariageForm, ActeDecesForm, LivretFamilleForm


class AccueilEtatCivilView(TemplateView):
    """Page d'accueil État Civil."""
    template_name = 'etat_civil/accueil.html'


class DemandeActeNaissanceView(CreateView):
    """Vue pour demander un acte de naissance."""
    model = ActeNaissance
    form_class = ActeNaissanceForm
    template_name = 'etat_civil/demande_naissance.html'
    
    def form_valid(self, form):
        acte = form.save(commit=False)
        if self.request.user.is_authenticated:
            acte.demandeur = self.request.user
        acte.save()
        messages.success(
            self.request, 
            f"Votre demande a été enregistrée. Numéro de suivi : {acte.numero_suivi}"
        )
        return redirect('etat_civil:suivi', numero_suivi=acte.numero_suivi)


class DemandeActeMariageView(CreateView):
    """Vue pour demander un acte de mariage."""
    model = ActeMariage
    form_class = ActeMariageForm
    template_name = 'etat_civil/demande_mariage.html'
    
    def form_valid(self, form):
        acte = form.save(commit=False)
        if self.request.user.is_authenticated:
            acte.demandeur = self.request.user
        acte.save()
        messages.success(
            self.request, 
            f"Votre demande a été enregistrée. Numéro de suivi : {acte.numero_suivi}"
        )
        return redirect('etat_civil:suivi', numero_suivi=acte.numero_suivi)


class DemandeActeDecesView(CreateView):
    """Vue pour demander un acte de décès."""
    model = ActeDeces
    form_class = ActeDecesForm
    template_name = 'etat_civil/demande_deces.html'
    
    def form_valid(self, form):
        acte = form.save(commit=False)
        if self.request.user.is_authenticated:
            acte.demandeur = self.request.user
        acte.save()
        messages.success(
            self.request, 
            f"Votre demande a été enregistrée. Numéro de suivi : {acte.numero_suivi}"
        )
        return redirect('etat_civil:suivi', numero_suivi=acte.numero_suivi)


class DemandeLivretFamilleView(CreateView):
    """Vue pour demander un livret de famille."""
    model = LivretFamille
    form_class = LivretFamilleForm
    template_name = 'etat_civil/demande_livret.html'
    
    def form_valid(self, form):
        acte = form.save(commit=False)
        if self.request.user.is_authenticated:
            acte.demandeur = self.request.user
        acte.save()
        messages.success(
            self.request, 
            f"Votre demande a été enregistrée. Numéro de suivi : {acte.numero_suivi}"
        )
        return redirect('etat_civil:suivi', numero_suivi=acte.numero_suivi)


def suivi_demande_view(request, numero_suivi=None):
    """Vue pour suivre une demande par numéro de suivi."""
    demande = None
    type_acte = None
    
    if numero_suivi:
        # Chercher dans tous les types d'actes
        for model, nom in [
            (ActeNaissance, 'Acte de naissance'),
            (ActeMariage, 'Acte de mariage'),
            (ActeDeces, 'Acte de décès'),
            (LivretFamille, 'Livret de famille')
        ]:
            try:
                demande = model.objects.get(numero_suivi=numero_suivi)
                type_acte = nom
                break
            except model.DoesNotExist:
                continue
    
    elif request.method == 'POST':
        numero = request.POST.get('numero_suivi', '').strip()
        if numero:
            return redirect('etat_civil:suivi', numero_suivi=numero)
    
    return render(request, 'etat_civil/suivi.html', {
        'demande': demande,
        'type_acte': type_acte,
        'numero_suivi': numero_suivi
    })


# Vues pour les agents (gestion des demandes)
@login_required
def liste_demandes_view(request):
    """Liste des demandes d'actes pour les agents."""
    if not request.user.can_manage_etat_civil():
        messages.error(request, "Vous n'avez pas accès à cette section.")
        return redirect('core:accueil')
    
    naissances = ActeNaissance.objects.all()[:20]
    mariages = ActeMariage.objects.all()[:20]
    deces = ActeDeces.objects.all()[:20]
    livrets = LivretFamille.objects.all()[:20]
    
    return render(request, 'etat_civil/agent/liste_demandes.html', {
        'naissances': naissances,
        'mariages': mariages,
        'deces': deces,
        'livrets': livrets,
    })


@login_required
def traiter_demande_view(request, type_acte, pk):
    """Vue pour traiter une demande."""
    if not request.user.can_manage_etat_civil():
        messages.error(request, "Vous n'avez pas accès à cette section.")
        return redirect('core:accueil')
    
    models_map = {
        'naissance': ActeNaissance,
        'mariage': ActeMariage,
        'deces': ActeDeces,
        'livret': LivretFamille,
    }
    
    Model = models_map.get(type_acte)
    if not Model:
        messages.error(request, "Type d'acte invalide.")
        return redirect('etat_civil:liste_demandes')
    
    demande = get_object_or_404(Model, pk=pk)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        commentaire = request.POST.get('commentaire', '')
        
        from django.utils import timezone
        
        if action == 'valider':
            demande.statut = 'valide'
            demande.agent_traitant = request.user
            demande.commentaire_agent = commentaire
            demande.date_traitement = timezone.now()
            demande.save()
            messages.success(request, "Demande validée avec succès.")
        
        elif action == 'rejeter':
            demande.statut = 'rejete'
            demande.agent_traitant = request.user
            demande.motif_rejet = commentaire
            demande.date_traitement = timezone.now()
            demande.save()
            messages.success(request, "Demande rejetée.")
        
        elif action == 'pret':
            demande.statut = 'pret'
            demande.save()
            messages.success(request, "Document marqué comme prêt pour retrait.")
        
        elif action == 'delivre':
            demande.statut = 'delivre'
            demande.date_delivrance = timezone.now()
            demande.save()
            messages.success(request, "Document marqué comme délivré.")
        
        return redirect('etat_civil:liste_demandes')
    
    return render(request, 'etat_civil/agent/traiter_demande.html', {
        'demande': demande,
        'type_acte': type_acte,
    })
