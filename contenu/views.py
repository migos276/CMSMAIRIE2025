"""
Vues pour la gestion du contenu.
"""
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import FileResponse
from .models import Article, Evenement, Document, ProjetMunicipal, Categorie


class ArticleListView(ListView):
    """Liste des articles publiés."""
    model = Article
    template_name = 'contenu/article_list.html'
    context_object_name = 'articles'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = Article.objects.filter(publie=True)
        categorie = self.request.GET.get('categorie')
        if categorie:
            queryset = queryset.filter(categorie__slug=categorie)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Categorie.objects.all()
        return context


class ArticleDetailView(DetailView):
    """Détail d'un article."""
    model = Article
    template_name = 'contenu/article_detail.html'
    context_object_name = 'article'
    
    def get_queryset(self):
        return Article.objects.filter(publie=True)
    
    def get_object(self):
        obj = super().get_object()
        obj.vues += 1
        obj.save(update_fields=['vues'])
        return obj


class EvenementListView(ListView):
    """Liste des événements."""
    model = Evenement
    template_name = 'contenu/evenement_list.html'
    context_object_name = 'evenements'
    paginate_by = 10
    
    def get_queryset(self):
        return Evenement.objects.filter(publie=True)


class EvenementDetailView(DetailView):
    """Détail d'un événement."""
    model = Evenement
    template_name = 'contenu/evenement_detail.html'
    context_object_name = 'evenement'
    
    def get_queryset(self):
        return Evenement.objects.filter(publie=True)


class DocumentListView(ListView):
    """Liste des documents publics."""
    model = Document
    template_name = 'contenu/document_list.html'
    context_object_name = 'documents'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Document.objects.filter(public=True)
        type_doc = self.request.GET.get('type')
        if type_doc:
            queryset = queryset.filter(type_document=type_doc)
        return queryset


def telecharger_document(request, pk):
    """Téléchargement d'un document."""
    document = get_object_or_404(Document, pk=pk, public=True)
    document.telechargements += 1
    document.save(update_fields=['telechargements'])
    return FileResponse(document.fichier, as_attachment=True)


class ProjetListView(ListView):
    """Liste des projets municipaux."""
    model = ProjetMunicipal
    template_name = 'contenu/projet_list.html'
    context_object_name = 'projets'
    paginate_by = 10
    
    def get_queryset(self):
        return ProjetMunicipal.objects.filter(publie=True)


class ProjetDetailView(DetailView):
    """Détail d'un projet municipal."""
    model = ProjetMunicipal
    template_name = 'contenu/projet_detail.html'
    context_object_name = 'projet'
    
    def get_queryset(self):
        return ProjetMunicipal.objects.filter(publie=True)
