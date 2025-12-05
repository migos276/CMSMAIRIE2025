#!/usr/bin/env python
"""
Script de test des routes du CMS E-MAIRIES (Version légère)
Teste tous les endpoints du projet Django
"""
import os
import sys
import json
from datetime import datetime
from pathlib import Path

# Ajouter le répertoire du projet au path
project_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(project_dir))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'e_cms.settings')

# Configuration minimale Django
import django
from django.conf import settings
settings.configure(
    DEBUG=True,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    },
    INSTALLED_APPS=[
        'django.contrib.contenttypes',
        'django.contrib.auth',
    ],
    SECRET_KEY='test-secret-key',
)

try:
    django.setup()
except Exception as e:
    pass

from django.urls import get_resolver, URLPattern, URLResolver
from django.test import Client

class RoutesTester:
    """Testeur de routes pour le CMS"""
    
    def __init__(self):
        self.client = Client()
        self.results = []
        self.passed = 0
        self.failed = 0
        self.routes_map = {}
        
    def extract_routes(self, patterns, prefix=''):
        """Extrait toutes les routes du URLconf"""
        routes = []
        
        for pattern in patterns:
            if isinstance(pattern, URLResolver):
                # C'est un include() avec sous-routes
                sub_prefix = prefix + str(pattern.pattern)
                if hasattr(pattern, 'url_patterns'):
                    routes.extend(self.extract_routes(pattern.url_patterns, sub_prefix))
            elif isinstance(pattern, URLPattern):
                # C'est une route individuelle
                route_path = prefix + str(pattern.pattern)
                routes.append({
                    'path': route_path,
                    'name': pattern.name,
                    'callback': pattern.callback if hasattr(pattern, 'callback') else None
                })
        
        return routes
    
    def get_all_routes(self):
        """Récupère toutes les routes du projet"""
        try:
            from django.urls import get_urlconf
            from importlib import import_module
            
            urlconf_module = import_module('e_cms.urls')
            patterns = urlconf_module.urlpatterns
            return self.extract_routes(patterns)
        except Exception as e:
            print(f"Erreur lors de l'extraction des routes: {e}")
            return []
    
    def test_route(self, route):
        """Teste une route spécifique"""
        try:
            url = route['path']
            name = route.get('name', 'unnamed')
            
            # Nettoyer l'URL pour éliminer les patterns Django
            url = url.replace('^', '').replace('$', '').replace('?P<', '<').replace('>', '>')
            
            # Éviter les paramètres obligatoires pour le test
            if '<' in url and '>' in url:
                # Remplacer les paramètres par des valeurs par défaut
                url = url.replace('<slug:slug>', 'test-slug')
                url = url.replace('<uuid:numero_suivi>', '00000000-0000-0000-0000-000000000000')
                url = url.replace('<uuid:numero>', '00000000-0000-0000-0000-000000000000')
                url = url.replace('<str:type_acte>', 'naissance')
                url = url.replace('<int:pk>', '1')
            
            if url.endswith('/') is False and url != '/':
                url += '/'
            
            # Tester la route
            response = self.client.get(url)
            
            # Considérer 200-399 comme succès
            success = 200 <= response.status_code < 400
            
            result = {
                'path': route['path'],
                'name': name,
                'url': url,
                'status': response.status_code,
                'success': success,
                'content_type': response.get('Content-Type', 'unknown')
            }
            
            self.results.append(result)
            if success:
                self.passed += 1
            else:
                self.failed += 1
            
            return result
            
        except Exception as e:
            result = {
                'path': route['path'],
                'name': route.get('name', 'unnamed'),
                'url': 'N/A',
                'status': 'ERROR',
                'error': str(e),
                'success': False
            }
            self.results.append(result)
            self.failed += 1
            return result
    
    def run_all_tests(self):
        """Exécute tous les tests de routes"""
        
        print("\n" + "="*100)
        print("ANALYSE DES ROUTES - E-CMS MAIRIES")
        print("="*100)
        print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        # Récupérer et analyser les routes
        routes = self.get_all_routes()
        
        if not routes:
            print("❌ Impossible de charger les routes depuis Django")
            print("Utilisation d'une analyse statique des fichiers urls.py\n")
            return self.static_analysis()
        
        print(f"� Total de routes trouvées: {len(routes)}\n")
        print("Exécution des tests...\n")
        
        # Grouper les routes par catégorie
        categories = {
            'admin': [],
            'api': [],
            'auth': [],
            'core': [],
            'etat_civil': [],
            'contenu': [],
            'services': [],
            'utilisateurs': [],
            'other': []
        }
        
        for route in routes:
            name = route.get('name', 'unnamed')
            path = route['path']
            
            if 'admin' in path or 'admin' in name:
                categories['admin'].append(route)
            elif 'api' in path or 'api' in name:
                categories['api'].append(route)
            elif any(x in name for x in ['connexion', 'deconnexion', 'inscription']):
                categories['auth'].append(route)
            elif 'etat_civil' in path or 'etat-civil' in path:
                categories['etat_civil'].append(route)
            elif 'contenu' in path:
                categories['contenu'].append(route)
            elif 'services' in path:
                categories['services'].append(route)
            elif 'utilisateurs' in path:
                categories['utilisateurs'].append(route)
            elif not path.startswith('/'):
                categories['core'].append(route)
            else:
                categories['other'].append(route)
        
        # Tester les routes par catégorie
        for category, routes_in_cat in categories.items():
            if routes_in_cat:
                print(f"\n� {category.upper()}: {len(routes_in_cat)} routes")
                print("-" * 100)
                for route in routes_in_cat[:10]:  # Limiter à 10 routes par catégorie
                    result = self.test_route(route)
                    status_symbol = "✅" if result['success'] else "❌"
                    print(f"  {status_symbol} {result['name']:<40} {result['status']:<5} {result['url']}")
                
                if len(routes_in_cat) > 10:
                    print(f"  ... et {len(routes_in_cat) - 10} autres routes")
        
        self.print_summary()
    
    def static_analysis(self):
        """Analyse statique des fichiers urls.py"""
        print("\n🔍 ANALYSE STATIQUE DES ROUTES\n")
        
        url_files = {
            'Core': '/home/menelas/Documents/GitHub/CMSMAIRIE2025/scripts/e_cms/core/urls.py',
            'État Civil': '/home/menelas/Documents/GitHub/CMSMAIRIE2025/scripts/e_cms/etat_civil/urls.py',
            'Contenu': '/home/menelas/Documents/GitHub/CMSMAIRIE2025/scripts/e_cms/contenu/urls.py',
            'Services': '/home/menelas/Documents/GitHub/CMSMAIRIE2025/scripts/e_cms/services/urls.py',
            'Utilisateurs': '/home/menelas/Documents/GitHub/CMSMAIRIE2025/scripts/e_cms/utilisateurs/urls.py',
        }
        
        total_routes = 0
        
        for category, filepath in url_files.items():
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # Compter les routes
                import re
                routes = re.findall(r"path\('([^']*)'", content)
                
                print(f"\n📋 {category}: {len(routes)} routes")
                print("-" * 100)
                
                for route in routes:
                    print(f"   • /{category.lower().replace(' ', '-')}/{route}")
                    total_routes += 1
                    
            except Exception as e:
                print(f"❌ Erreur lors de la lecture de {filepath}: {e}")
        
        # Routes principales (admin, api)
        print(f"\n📋 ROUTES PRINCIPALES: 5+ routes")
        print("-" * 100)
        print(f"   • /admin/")
        print(f"   • /cms-admin/")
        print(f"   • /documents/")
        print(f"   • /api/v2/")
        print(f"   • / (Wagtail pages)")
        
        total_routes += 5
        
        print(f"\n\n{'='*100}")
        print("RÉSUMÉ DE L'ANALYSE STATIQUE")
        print(f"{'='*100}")
        print(f"\n📊 Total de routes identifiées: {total_routes}")
        
        return total_routes
    
    def print_summary(self):
        """Affiche un résumé des tests"""
        print("\n" + "="*100)
        print("RÉSUMÉ DES TESTS")
        print("="*100)
        
        if self.results:
            print(f"\n✅ Routes réussies: {self.passed}")
            print(f"❌ Routes échouées: {self.failed}")
            print(f"📊 Total: {self.passed + self.failed}")
            print(f"📈 Taux de réussite: {(self.passed / (self.passed + self.failed) * 100) if (self.passed + self.failed) > 0 else 0:.1f}%")
            
            print("\n" + "="*100)
            print("DÉTAILS DES RÉSULTATS")
            print("="*100)
            
            # Groupe par statut
            status_groups = {}
            for result in self.results:
                status = result['status']
                if status not in status_groups:
                    status_groups[status] = []
                status_groups[status].append(result)
            
            # Affiche réussis
            if 200 in status_groups:
                print("\n✅ ROUTES 200 OK:")
                for result in status_groups[200]:
                    print(f"   {result['name']:<40} {result['url']}")
            
            # Affiche redirections
            redirects = [s for s in status_groups.keys() if 300 <= s < 400]
            if redirects:
                print("\n🔄 REDIRECTIONS (3xx):")
                for status in sorted(redirects):
                    for result in status_groups[status]:
                        print(f"   {result['name']:<40} → {result['status']}")
            
            # Affiche erreurs
            if 404 in status_groups:
                print("\n❌ ROUTES 404 NOT FOUND:")
                for result in status_groups[404]:
                    print(f"   {result['name']:<40} {result['url']}")
            
            if 'ERROR' in status_groups:
                print("\n⚠️  ERREURS:")
                for result in status_groups['ERROR']:
                    print(f"   {result['name']:<40}")
                    print(f"      → {result.get('error', 'Erreur inconnue')}")
        
        print("\n" + "="*100)

def main():
    """Fonction principale"""
    tester = RoutesTester()
    
    try:
        tester.run_all_tests()
    except Exception as e:
        print(f"\n❌ Erreur lors de l'exécution: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
