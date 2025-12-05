"""
Template tags personnalisés pour le CMS Wagtail.
"""
from django import template
from django.template.loader import render_to_string

from wagtail.models import Site

from cms.models import (
    MenuPrincipal, ConfigurationMairie, Partenaire,
    ServiceMairie, FAQ
)

register = template.Library()


@register.simple_tag(takes_context=True)
def get_site_root(context):
    """Récupère la page racine du site actuel."""
    request = context.get('request')
    if request:
        site = Site.find_for_request(request)
        if site:
            return site.root_page
    return None


@register.simple_tag(takes_context=True)
def get_config_mairie(context):
    """Récupère la configuration de la mairie."""
    request = context.get('request')
    if request:
        site = Site.find_for_request(request)
        if site:
            return ConfigurationMairie.for_site(site)
    return None


@register.inclusion_tag('cms/tags/menu_principal.html', takes_context=True)
def menu_principal(context):
    """Affiche le menu principal."""
    menus = MenuPrincipal.objects.prefetch_related('items__lien_page').all()
    return {
        'menus': menus,
        'request': context.get('request'),
    }


@register.inclusion_tag('cms/tags/breadcrumb.html', takes_context=True)
def breadcrumb(context):
    """Affiche le fil d'Ariane."""
    self = context.get('self')
    if self:
        ancestors = self.get_ancestors()[1:]  # Exclure la racine
        return {
            'ancestors': ancestors,
            'current_page': self,
            'request': context.get('request'),
        }
    return {}


@register.inclusion_tag('cms/tags/footer.html', takes_context=True)
def footer(context):
    """Affiche le footer avec les informations de la mairie."""
    request = context.get('request')
    site = Site.find_for_request(request) if request else None
    config = ConfigurationMairie.for_site(site) if site else None
    partenaires = Partenaire.objects.filter(actif=True)[:8]
    
    return {
        'config': config,
        'partenaires': partenaires,
        'request': request,
    }


@register.inclusion_tag('cms/tags/services_widget.html')
def services_widget(limit=6):
    """Widget des services de la mairie."""
    services = ServiceMairie.objects.filter(actif=True)[:limit]
    return {'services': services}


@register.inclusion_tag('cms/tags/faq_widget.html')
def faq_widget(categorie=None, limit=5):
    """Widget FAQ."""
    faqs = FAQ.objects.filter(publie=True)
    if categorie:
        faqs = faqs.filter(categorie=categorie)
    return {'faqs': faqs[:limit]}


@register.simple_tag
def get_partenaires(limit=10):
    """Récupère les partenaires actifs."""
    return Partenaire.objects.filter(actif=True)[:limit]


@register.filter
def format_fcfa(value):
    """Formate un montant en FCFA."""
    try:
        value = int(value)
        return '{:,.0f} FCFA'.format(value).replace(',', ' ')
    except (ValueError, TypeError):
        return value


@register.filter
def icon_class(icon_name):
    """Convertit un nom d'icône en classe CSS."""
    icon_map = {
        'users': 'fa-users',
        'file-text': 'fa-file-text',
        'calendar': 'fa-calendar',
        'home': 'fa-home',
        'phone': 'fa-phone',
        'mail': 'fa-envelope',
        'map': 'fa-map-marker',
        'clock': 'fa-clock',
        'check': 'fa-check-circle',
        'alert': 'fa-exclamation-triangle',
    }
    return icon_map.get(icon_name, f'fa-{icon_name}')
