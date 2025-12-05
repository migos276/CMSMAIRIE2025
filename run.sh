#!/bin/bash
# Script de démarrage rapide pour E-CMS

set -e

# Couleurs
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

PROJECT_ROOT="/home/menelas/Documents/GitHub/CMSMAIRIE2025"
APP_DIR="$PROJECT_ROOT/scripts/e_cms"
PYTHON="$PROJECT_ROOT/env/bin/python"
MANAGE="$PYTHON manage.py"

cd "$APP_DIR"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}🚀 E-CMS - Script de Démarrage${NC}"
echo -e "${BLUE}========================================${NC}\n"

# Fonction pour afficher les options
show_menu() {
    echo -e "${YELLOW}Choisissez une action:${NC}"
    echo "1) Démarrer le serveur"
    echo "2) Migrations base de données"
    echo "3) Créer un superutilisateur"
    echo "4) Vérifier la configuration"
    echo "5) Lancer les tests"
    echo "6) Collecter les fichiers statiques"
    echo "7) Ouvrir l'admin Django"
    echo "8) Shell Django"
    echo "0) Quitter"
    echo ""
}

# Menu principal
while true; do
    show_menu
    read -p "Votre choix: " choice
    
    case $choice in
        1)
            echo -e "\n${GREEN}▶️ Démarrage du serveur...${NC}\n"
            $MANAGE runserver 0.0.0.0:8000
            ;;
        2)
            echo -e "\n${GREEN}▶️ Exécution des migrations...${NC}\n"
            $MANAGE migrate
            echo -e "\n${GREEN}✅ Migrations appliquées!${NC}\n"
            ;;
        3)
            echo -e "\n${GREEN}▶️ Création d'un superutilisateur...${NC}\n"
            $PYTHON create_admin.py
            echo -e "\n${GREEN}✅ Superutilisateur créé!${NC}\n"
            ;;
        4)
            echo -e "\n${GREEN}▶️ Vérification de la configuration...${NC}\n"
            $MANAGE check
            echo -e "\n${GREEN}✅ Configuration OK!${NC}\n"
            ;;
        5)
            echo -e "\n${GREEN}▶️ Lancement des tests...${NC}\n"
            $MANAGE test
            echo -e "\n${GREEN}✅ Tests terminés!${NC}\n"
            ;;
        6)
            echo -e "\n${GREEN}▶️ Collecte des fichiers statiques...${NC}\n"
            $MANAGE collectstatic --noinput
            echo -e "\n${GREEN}✅ Fichiers statiques collectés!${NC}\n"
            ;;
        7)
            echo -e "\n${GREEN}▶️ Ouverture de l'admin Django...${NC}\n"
            echo "Allez à: http://localhost:8000/admin/"
            echo "Email: admin@example.com"
            echo "Mot de passe: admin123"
            echo ""
            ;;
        8)
            echo -e "\n${GREEN}▶️ Shell Django...${NC}\n"
            $MANAGE shell
            ;;
        0)
            echo -e "\n${GREEN}Au revoir!${NC}\n"
            exit 0
            ;;
        *)
            echo -e "\n${YELLOW}❌ Choix invalide${NC}\n"
            ;;
    esac
done
