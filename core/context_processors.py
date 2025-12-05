"""
Context processors pour injecter les données de la mairie dans les templates.
"""
from django.db import connection


def mairie_context(request):
    """Injecte les informations de la mairie courante dans le contexte."""
    context = {}
    
    if hasattr(connection, 'tenant'):
        mairie = connection.tenant
        context['mairie'] = {
            'nom': mairie.nom,
            'code': mairie.code,
            'region': mairie.region,
            'departement': mairie.departement,
            'arrondissement': mairie.arrondissement,
            'adresse': mairie.adresse,
            'telephone': mairie.telephone,
            'email': mairie.email,
            'logo': mairie.logo.url if mairie.logo else None,
            'couleur_primaire': mairie.couleur_primaire,
            'couleur_secondaire': mairie.couleur_secondaire,
        }
    
    return context
