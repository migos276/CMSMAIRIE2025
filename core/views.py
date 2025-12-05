"""
Vues principales du CMS.
"""
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, DetailView
from contenu.models import Article, Evenement, Document
from services.models import DemandeActe
from .models import PageStatique


class AccueilView(TemplateView):
    """Page d'accueil expliquant nos services de création de sites web."""
    template_name = 'core/accueil_services.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articles_recents'] = Article.objects.filter(publie=True).order_by('-date_publication')[:5]
        context['evenements_prochains'] = Evenement.objects.filter(publie=True).order_by('date_debut')[:5]
        context['documents_recents'] = Document.objects.filter(public=True).order_by('-date_ajout')[:5]
        return context
class AccueilView2(TemplateView):
    """Page d'accueil expliquant nos services de création de sites web."""
    template_name = 'core/accueil_services.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articles_recents'] = Article.objects.filter(publie=True).order_by('-date_publication')[:5]
        context['evenements_prochains'] = Evenement.objects.filter(publie=True).order_by('date_debut')[:5]
        context['documents_recents'] = Document.objects.filter(public=True).order_by('-date_ajout')[:5]
        return context


class PageStatiqueView(DetailView):
    """Affichage d'une page statique."""
    model = PageStatique
    template_name = 'core/page_statique.html'
    context_object_name = 'page'
    
    def get_queryset(self):
        return PageStatique.objects.filter(publie=True)


class TableauDeBordView(TemplateView):
    """Tableau de bord pour les agents municipaux."""
    template_name = 'core/tableau_de_bord.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['demandes_en_attente'] = DemandeActe.objects.filter(statut='en_attente').count()
        context['demandes_en_cours'] = DemandeActe.objects.filter(statut='en_cours').count()
        context['articles_total'] = Article.objects.count()
        return context
