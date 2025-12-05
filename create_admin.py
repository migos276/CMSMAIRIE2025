#!/usr/bin/env python
"""Créer un superutilisateur admin pour E-CMS"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'e_cms.settings')
django.setup()

from utilisateurs.models import Utilisateur

# Vérifier si l'utilisateur existe déjà
if not Utilisateur.objects.filter(email='admin@example.com').exists():
    Utilisateur.objects.create_superuser(
        email='admin@example.com',
        password='admin123',
        first_name='Admin',
        last_name='E-CMS'
    )
    print("✅ Superutilisateur 'admin' créé avec succès !")
    print("   Email: admin@example.com")
    print("   Mot de passe: admin123")
else:
    print("ℹ️  L'utilisateur admin existe déjà")

# Afficher les utilisateurs
print("\n📋 Utilisateurs actuels:")
for user in Utilisateur.objects.all():
    print(f"  - {user.email} (superuser: {user.is_superuser})")
