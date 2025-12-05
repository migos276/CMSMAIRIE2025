"""
Script pour créer des données de test.
À exécuter après les migrations.
"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'e_cms.settings')
django.setup()

from tenants.models import Mairie, Domaine
from django_tenants.utils import schema_context


def create_sample_mairies():
    """Créer des mairies de test."""
    
    mairies_data = [
        {
            'nom': 'Mairie de Yaoundé 2',
            'code': 'yaounde2',
            'region': 'Centre',
            'departement': 'Mfoundi',
            'arrondissement': 'Yaoundé 2',
            'adresse': 'Avenue Kennedy, Yaoundé',
            'telephone': '+237 222 23 45 67',
            'email': 'mairie-yaounde2@arited.cm',
            'schema_name': 'yaounde2',
            'domain': 'mairie-yaounde2.localhost',
        },
        {
            'nom': 'Mairie de Douala 5',
            'code': 'douala5',
            'region': 'Littoral',
            'departement': 'Wouri',
            'arrondissement': 'Douala 5',
            'adresse': 'Rue des Manguiers, Douala',
            'telephone': '+237 233 45 67 89',
            'email': 'mairie-douala5@arited.cm',
            'schema_name': 'douala5',
            'domain': 'mairie-douala5.localhost',
        },
        {
            'nom': 'Mairie de Bafoussam',
            'code': 'bafoussam',
            'region': 'Ouest',
            'departement': 'Mifi',
            'arrondissement': 'Bafoussam 1er',
            'adresse': 'Place de l\'Indépendance, Bafoussam',
            'telephone': '+237 233 44 55 66',
            'email': 'mairie-bafoussam@arited.cm',
            'schema_name': 'bafoussam',
            'domain': 'mairie-bafoussam.localhost',
        },
    ]
    
    for data in mairies_data:
        domain = data.pop('domain')
        
        mairie, created = Mairie.objects.get_or_create(
            code=data['code'],
            defaults=data
        )
        
        if created:
            print(f"✅ Mairie créée : {mairie.nom}")
            
            # Créer le domaine
            Domaine.objects.get_or_create(
                domain=domain,
                tenant=mairie,
                defaults={'is_primary': True}
            )
            print(f"   → Domaine : {domain}")
        else:
            print(f"ℹ️  Mairie existante : {mairie.nom}")


if __name__ == '__main__':
    print("🏛️ Création des mairies de test...")
    create_sample_mairies()
    print("\n✅ Terminé !")
