from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.AccueilView2.as_view(), name='accueil'),
    path('tableau-de-bord/', views.TableauDeBordView.as_view(), name='tableau_de_bord'),
    path('page/<slug:slug>/', views.PageStatiqueView.as_view(), name='page_statique'),
]
