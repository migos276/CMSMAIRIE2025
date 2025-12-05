#!/usr/bin/env python
"""
Script de test complet E-CMS MAIRIE 2025
Valide tous les éléments clés de l'application
"""
import os
import sys
import django

os.chdir(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'e_cms.settings')
django.setup()

from django.test import Client
from utilisateurs.models import Utilisateur
from etat_civil.models import ActeNaissance
from services.models import RendezVous

def print_header(text):
    """Affiche un header formaté."""
    print(f"\n{'='*80}")
    print(f"🧪 {text}")
    print(f"{'='*80}\n")

def print_result(name, passed, message=""):
    """Affiche le résultat d'un test."""
    status = "✅ PASS" if passed else "❌ FAIL"
    print(f"{status} | {name:<50} {message}")

def test_admin():
    """Teste l'accès Django Admin."""
    print_header("TEST 1: ADMIN INTERFACES")
    
    client = Client()
    
    # Vérifier admin user
    try:
        user = Utilisateur.objects.get(email='admin@example.com')
        print_result("Admin User Exists", True, f"({user.email})")
    except:
        user = Utilisateur.objects.create_superuser(
            email='admin@example.com',
            password='admin123'
        )
        print_result("Admin User Created", True, f"({user.email})")
    
    # Test Django Admin
    client.force_login(user)
    response = client.get('/admin/')
    print_result("Django Admin Access", response.status_code == 200, f"Status: {response.status_code}")
    
    # Test Wagtail Admin
    response = client.get('/cms-admin/')
    print_result("Wagtail Admin Access", response.status_code == 200, f"Status: {response.status_code}")

def test_authentication():
    """Teste l'authentification."""
    print_header("TEST 2: AUTHENTICATION")
    
    client = Client()
    
    # Inscription
    user_data = {
        'email': 'test_auth@example.fr',
        'first_name': 'Test',
        'last_name': 'Auth',
        'telephone': '0600000000',
        'cni': 'TEST001',
        'password1': 'TestPass123!',
        'password2': 'TestPass123!',
    }
    
    response = client.post('/utilisateurs/inscription/', user_data, follow=True)
    print_result("User Registration", response.status_code == 200, f"Status: {response.status_code}")
    
    # Connexion
    login_data = {
        'email': 'test_auth@example.fr',
        'password': 'TestPass123!',
    }
    
    response = client.post('/utilisateurs/connexion/', login_data, follow=True)
    is_authenticated = response.wsgi_request.user.is_authenticated
    print_result("User Login", is_authenticated, "User authenticated")
    
    # Protected route
    response = client.get('/tableau-de-bord/')
    print_result("Protected Route Access", response.status_code == 200, f"Status: {response.status_code}")
    
    # Profil
    response = client.get('/utilisateurs/profil/')
    print_result("User Profile Access", response.status_code == 200, f"Status: {response.status_code}")
    
    # Logout
    response = client.get('/utilisateurs/deconnexion/', follow=True)
    is_authenticated = response.wsgi_request.user.is_authenticated
    print_result("User Logout", not is_authenticated, "User logged out")

def test_frontend_routes():
    """Teste toutes les routes frontend."""
    print_header("TEST 3: FRONTEND ROUTES")
    
    client = Client()
    routes = [
        ('/', 'Home'),
        ('/tableau-de-bord/', 'Dashboard'),
        ('/utilisateurs/connexion/', 'Login'),
        ('/utilisateurs/inscription/', 'Registration'),
        ('/etat-civil/', 'État Civil Home'),
        ('/etat-civil/naissance/', 'Birth Act Request'),
        ('/etat-civil/mariage/', 'Marriage Act Request'),
        ('/etat-civil/deces/', 'Death Act Request'),
        ('/etat-civil/livret-famille/', 'Family Booklet'),
        ('/services/', 'Services Home'),
        ('/services/rendez-vous/', 'Appointment'),
        ('/services/reclamation/', 'Complaint'),
        ('/contenu/articles/', 'Articles'),
        ('/contenu/evenements/', 'Events'),
        ('/contenu/documents/', 'Documents'),
        ('/contenu/projets/', 'Projects'),
    ]
    
    passed = 0
    for route, name in routes:
        response = client.get(route)
        is_ok = response.status_code == 200
        print_result(f"Route: {name:<30}", is_ok, f"{route:<35} → {response.status_code}")
        if is_ok:
            passed += 1
    
    print(f"\n✅ Total: {passed}/{len(routes)} routes OK")

def test_forms_etat_civil():
    """Teste les formulaires État Civil."""
    print_header("TEST 4: ÉTAT CIVIL FORMS")
    
    client = Client()
    
    form_data = {
        'type_acte': 'extrait',
        'demandeur_nom': 'Dupont',
        'demandeur_prenom': 'Jean',
        'demandeur_telephone': '0600000001',
        'demandeur_email': 'jean@example.fr',
        'nom_concerne': 'Dupont',
        'prenom_concerne': 'Michel',
        'date_naissance': '1990-05-15',
        'lieu_naissance': 'Paris',
        'nom_pere': 'Dupont',
        'prenom_pere': 'Pierre',
        'nom_mere': 'Martin',
        'prenom_mere': 'Anne',
    }
    
    # Test submission
    response = client.post('/etat-civil/naissance/', form_data, follow=True)
    
    naissance_exists = ActeNaissance.objects.filter(
        nom_concerne='Dupont',
        prenom_concerne='Michel'
    ).exists()
    
    print_result("Birth Act Form Submission", response.status_code == 200, f"Status: {response.status_code}")
    print_result("Birth Act Saved to DB", naissance_exists, "Record exists")
    
    if naissance_exists:
        acte = ActeNaissance.objects.get(nom_concerne='Dupont', prenom_concerne='Michel')
        print_result("Birth Act UUID Generated", bool(acte.numero_suivi), f"UUID: {acte.numero_suivi}")
        print_result("Birth Act Status", acte.statut == 'en_attente', f"Status: {acte.statut}")

def test_forms_services():
    """Teste les formulaires Services."""
    print_header("TEST 5: SERVICES FORMS")
    
    client = Client()
    
    rdv_data = {
        'type_rdv': 1,  # Devrait être le premier type
        'nom': 'Dupont',
        'prenom': 'Pierre',
        'telephone': '0600000002',
        'email': 'pierre@example.fr',
        'date': '2025-01-15',
        'heure': '14:00',
        'motif': 'Consultation générale',
    }
    
    response = client.get('/services/rendez-vous/')
    print_result("Appointment Form Display", response.status_code == 200, f"Status: {response.status_code}")
    
    response = client.get('/services/reclamation/')
    print_result("Complaint Form Display", response.status_code == 200, f"Status: {response.status_code}")

def test_database():
    """Teste la base de données."""
    print_header("TEST 6: DATABASE")
    
    try:
        user_count = Utilisateur.objects.count()
        print_result("Utilisateurs Table", True, f"{user_count} users")
    except Exception as e:
        print_result("Utilisateurs Table", False, str(e))
    
    try:
        naissance_count = ActeNaissance.objects.count()
        print_result("ActeNaissance Table", True, f"{naissance_count} records")
    except Exception as e:
        print_result("ActeNaissance Table", False, str(e))
    
    try:
        from django.core.management import call_command
        from io import StringIO
        out = StringIO()
        call_command('check', stdout=out)
        print_result("Django System Check", True, "0 errors")
    except Exception as e:
        print_result("Django System Check", False, str(e))

def main():
    """Exécute tous les tests."""
    print("\n" + "="*80)
    print("🚀 E-CMS MAIRIE 2025 - COMPREHENSIVE TEST SUITE")
    print("="*80)
    
    test_admin()
    test_authentication()
    test_frontend_routes()
    test_forms_etat_civil()
    test_forms_services()
    test_database()
    
    print("\n" + "="*80)
    print("✅ ALL TESTS COMPLETED")
    print("="*80 + "\n")
    
    print("📌 NEXT STEPS:")
    print("  1. Start server: python manage.py runserver 0.0.0.0:8001")
    print("  2. Access frontend: http://localhost:8001/")
    print("  3. Access CMS: http://localhost:8001/cms-admin/")
    print("  4. Admin credentials: admin@example.com / admin123")
    print("")

if __name__ == '__main__':
    main()
