from django.urls import path
from . import views

app_name = 'contenu'

urlpatterns = [
    # Articles
    path('articles/', views.ArticleListView.as_view(), name='article_list'),
    path('articles/<slug:slug>/', views.ArticleDetailView.as_view(), name='article_detail'),
    
    # Événements
    path('evenements/', views.EvenementListView.as_view(), name='evenement_list'),
    path('evenements/<slug:slug>/', views.EvenementDetailView.as_view(), name='evenement_detail'),
    
    # Documents
    path('documents/', views.DocumentListView.as_view(), name='document_list'),
    path('documents/<int:pk>/telecharger/', views.telecharger_document, name='telecharger_document'),
    
    # Projets
    path('projets/', views.ProjetListView.as_view(), name='projet_list'),
    path('projets/<slug:slug>/', views.ProjetDetailView.as_view(), name='projet_detail'),
]
