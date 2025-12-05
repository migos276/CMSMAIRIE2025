"""
Django + Wagtail settings for E-CMS project.
CMS multisite dédié aux mairies du Cameroun
Intégration Wagtail 6.2 + django-tenants
"""

from pathlib import Path
import os
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

# Charger le fichier .env
load_dotenv(BASE_DIR / '.env')

SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-dev-key-change-in-production')

DEBUG = os.environ.get('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Wagtail apps
    'wagtail.contrib.forms',
    'wagtail.contrib.redirects',
    'wagtail.contrib.settings',
    'wagtail.contrib.styleguide',
    'wagtail.contrib.routable_page',
    'wagtail.contrib.search_promotions',
    'wagtail.embeds',
    'wagtail.sites',
    'wagtail.users',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail.images',
    'wagtail.search',
    'wagtail.admin',
    'wagtail',
    
    # Third party
    'modelcluster',
    'taggit',
    'rest_framework',
    
    # E-CMS apps
    'core',
    'cms',
    'etat_civil',
    'contenu',
    'services',
    'utilisateurs',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'wagtail.contrib.redirects.middleware.RedirectMiddleware',
]

ROOT_URLCONF = 'e_cms.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.mairie_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'e_cms.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / os.environ.get('DB_NAME', 'db.sqlite3'),
    }
}

# Auth
AUTH_USER_MODEL = 'utilisateurs.Utilisateur'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Africa/Douala'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Login settings
LOGIN_URL = '/connexion/'
LOGIN_REDIRECT_URL = '/tableau-de-bord/'
LOGOUT_REDIRECT_URL = '/'

# =============================================================================
# WAGTAIL CONFIGURATION
# =============================================================================

WAGTAIL_SITE_NAME = 'E-CMS Mairies du Cameroun'

# Base URL pour Wagtail (utilisé pour les emails, etc.)
WAGTAILADMIN_BASE_URL = os.environ.get('WAGTAIL_BASE_URL', 'http://localhost')

# Recherche Wagtail
WAGTAILSEARCH_BACKENDS = {
    'default': {
        'BACKEND': 'wagtail.search.backends.database',
    }
}

# Configuration des images Wagtail
WAGTAILIMAGES_IMAGE_MODEL = 'cms.ImagePersonnalisee'

# Configuration des documents Wagtail
WAGTAILDOCS_DOCUMENT_MODEL = 'cms.DocumentPersonnalise'

# Formats d'images personnalisés
WAGTAILIMAGES_FORMAT_CONVERSIONS = {
    'bmp': 'jpeg',
    'webp': 'webp',
}

# Taille max upload (10MB)
WAGTAILIMAGES_MAX_UPLOAD_SIZE = 10 * 1024 * 1024

# Configuration des embeds
WAGTAILEMBEDS_FINDERS = [
    {
        'class': 'wagtail.embeds.finders.oembed',
    }
]

# Configuration du rich text editor
WAGTAILADMIN_RICH_TEXT_EDITORS = {
    'default': {
        'WIDGET': 'wagtail.admin.rich_text.DraftailRichTextArea',
        'OPTIONS': {
            'features': [
                'h2', 'h3', 'h4',
                'bold', 'italic', 'strikethrough',
                'ol', 'ul',
                'blockquote',
                'link', 'document-link',
                'image', 'embed',
                'hr',
            ]
        }
    },
}

# Password required pour les pages protégées
WAGTAIL_PASSWORD_MANAGEMENT_ENABLED = True
WAGTAIL_PASSWORD_RESET_ENABLED = True

# Moderation workflow
WAGTAIL_MODERATION_ENABLED = True

# Internationalisation Wagtail
WAGTAIL_I18N_ENABLED = True
WAGTAIL_CONTENT_LANGUAGES = [
    ('fr', 'Français'),
    ('en', 'English'),
]

# Configuration des formulaires Wagtail
WAGTAILFORMS_HELP_TEXT_ALLOW_HTML = True

# API Wagtail
WAGTAILAPI_BASE_URL = '/api/v2/'
WAGTAILAPI_LIMIT_MAX = 100

# Configuration de l'admin Wagtail
WAGTAILADMIN_NOTIFICATION_USE_HTML = True
WAGTAILADMIN_NOTIFICATION_INCLUDE_SUPERUSERS = True

# Slugs en français
WAGTAIL_ALLOW_UNICODE_SLUGS = True

# Date/Time format
WAGTAIL_DATE_FORMAT = '%d/%m/%Y'
WAGTAIL_DATETIME_FORMAT = '%d/%m/%Y %H:%M'
WAGTAIL_TIME_FORMAT = '%H:%M'

# =============================================================================
# REST FRAMEWORK
# =============================================================================

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}
