"""
Modèles Wagtail pour le CMS E-CMS.
Pages, snippets, blocs et modèles personnalisés.
"""
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.models import ClusterableModel
from taggit.models import TaggedItemBase

from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import (
    FieldPanel, MultiFieldPanel, InlinePanel, 
    FieldRowPanel, PageChooserPanel, TabbedInterface, ObjectList
)
from wagtail.search import index
from wagtail.snippets.models import register_snippet
from wagtail.images.models import Image, AbstractImage, AbstractRendition
from wagtail.documents.models import Document, AbstractDocument
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting

from .blocks import (
    HeroBlock, CardsBlock, CTABlock, GalerieBlock,
    AccordionBlock, TimelineBlock, StatsBlock, TeamBlock,
    ContactBlock, MapBlock, ServicesBlock, TestimonialsBlock,
    RichTextBlock, ImageTextBlock, VideoBlock, DocumentsBlock
)


# =============================================================================
# IMAGES ET DOCUMENTS PERSONNALISÉS
# =============================================================================

class ImagePersonnalisee(AbstractImage):
    """Image personnalisée avec métadonnées supplémentaires."""
    legende = models.CharField(max_length=255, blank=True, verbose_name="Légende")
    credit = models.CharField(max_length=255, blank=True, verbose_name="Crédit photo")
    
    admin_form_fields = Image.admin_form_fields + ('legende', 'credit',)

    class Meta:
        verbose_name = "Image"
        verbose_name_plural = "Images"


class ImagePersonnaliseeRendition(AbstractRendition):
    """Renditions pour les images personnalisées."""
    image = models.ForeignKey(
        ImagePersonnalisee, 
        on_delete=models.CASCADE, 
        related_name='renditions'
    )

    class Meta:
        unique_together = (('image', 'filter_spec', 'focal_point_key'),)


class DocumentPersonnalise(AbstractDocument):
    """Document personnalisé avec métadonnées supplémentaires."""
    description = models.TextField(blank=True, verbose_name="Description")
    categorie = models.CharField(max_length=100, blank=True, verbose_name="Catégorie")
    date_document = models.DateField(null=True, blank=True, verbose_name="Date du document")
    
    admin_form_fields = Document.admin_form_fields + ('description', 'categorie', 'date_document',)

    class Meta:
        verbose_name = "Document"
        verbose_name_plural = "Documents"


# =============================================================================
# PARAMÈTRES DU SITE (WAGTAIL SETTINGS)
# =============================================================================

@register_setting
class ConfigurationMairie(BaseSiteSetting):
    """Configuration globale de la mairie."""
    
    # Identité
    nom_mairie = models.CharField(max_length=200, verbose_name="Nom de la mairie")
    slogan = models.CharField(max_length=300, blank=True, verbose_name="Slogan")
    logo = models.ForeignKey(
        'cms.ImagePersonnalisee',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="Logo"
    )
    favicon = models.ForeignKey(
        'cms.ImagePersonnalisee',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="Favicon"
    )
    
    # Coordonnées
    adresse = models.TextField(blank=True, verbose_name="Adresse")
    telephone = models.CharField(max_length=50, blank=True, verbose_name="Téléphone")
    email = models.EmailField(blank=True, verbose_name="Email")
    
    # Réseaux sociaux
    facebook = models.URLField(blank=True, verbose_name="Facebook")
    twitter = models.URLField(blank=True, verbose_name="Twitter/X")
    instagram = models.URLField(blank=True, verbose_name="Instagram")
    youtube = models.URLField(blank=True, verbose_name="YouTube")
    linkedin = models.URLField(blank=True, verbose_name="LinkedIn")
    
    # Horaires
    horaires = RichTextField(blank=True, verbose_name="Horaires d'ouverture")
    
    # Couleurs (personnalisation visuelle)
    couleur_primaire = models.CharField(
        max_length=7, default='#1E40AF', 
        verbose_name="Couleur primaire",
        help_text="Code hexadécimal (ex: #1E40AF)"
    )
    couleur_secondaire = models.CharField(
        max_length=7, default='#059669',
        verbose_name="Couleur secondaire"
    )
    couleur_accent = models.CharField(
        max_length=7, default='#F59E0B',
        verbose_name="Couleur d'accent"
    )
    
    # SEO
    meta_description = models.TextField(
        blank=True, 
        verbose_name="Description SEO",
        help_text="Description pour les moteurs de recherche"
    )
    
    # Analytics
    google_analytics_id = models.CharField(
        max_length=50, blank=True,
        verbose_name="ID Google Analytics"
    )

    panels = [
        MultiFieldPanel([
            FieldPanel('nom_mairie'),
            FieldPanel('slogan'),
            FieldPanel('logo'),
            FieldPanel('favicon'),
        ], heading="Identité"),
        MultiFieldPanel([
            FieldPanel('adresse'),
            FieldPanel('telephone'),
            FieldPanel('email'),
        ], heading="Coordonnées"),
        MultiFieldPanel([
            FieldPanel('facebook'),
            FieldPanel('twitter'),
            FieldPanel('instagram'),
            FieldPanel('youtube'),
            FieldPanel('linkedin'),
        ], heading="Réseaux sociaux"),
        MultiFieldPanel([
            FieldPanel('horaires'),
        ], heading="Horaires"),
        MultiFieldPanel([
            FieldPanel('couleur_primaire'),
            FieldPanel('couleur_secondaire'),
            FieldPanel('couleur_accent'),
        ], heading="Personnalisation visuelle"),
        MultiFieldPanel([
            FieldPanel('meta_description'),
            FieldPanel('google_analytics_id'),
        ], heading="SEO & Analytics"),
    ]

    class Meta:
        verbose_name = "Configuration de la mairie"


# =============================================================================
# SNIPPETS (ÉLÉMENTS RÉUTILISABLES)
# =============================================================================

@register_snippet
class MenuPrincipal(ClusterableModel):
    """Menu de navigation principal."""
    titre = models.CharField(max_length=100)
    ordre = models.PositiveIntegerField(default=0)
    
    class Meta:
        verbose_name = "Menu principal"
        verbose_name_plural = "Menus principaux"
        ordering = ['ordre']
    
    def __str__(self):
        return self.titre
    
    panels = [
        FieldPanel('titre'),
        FieldPanel('ordre'),
        InlinePanel('items', label="Éléments du menu"),
    ]


class MenuItem(Orderable):
    """Élément de menu."""
    menu = ParentalKey(MenuPrincipal, on_delete=models.CASCADE, related_name='items')
    titre = models.CharField(max_length=100, verbose_name="Titre")
    lien_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="Page interne"
    )
    lien_externe = models.URLField(blank=True, verbose_name="Lien externe")
    ouvrir_nouvel_onglet = models.BooleanField(default=False)
    
    @property
    def lien(self):
        if self.lien_page:
            return self.lien_page.url
        return self.lien_externe
    
    panels = [
        FieldPanel('titre'),
        PageChooserPanel('lien_page'),
        FieldPanel('lien_externe'),
        FieldPanel('ouvrir_nouvel_onglet'),
    ]


@register_snippet
class Partenaire(models.Model):
    """Partenaires et sponsors."""
    nom = models.CharField(max_length=200)
    logo = models.ForeignKey(
        'cms.ImagePersonnalisee',
        on_delete=models.CASCADE,
        related_name='+'
    )
    site_web = models.URLField(blank=True)
    ordre = models.PositiveIntegerField(default=0)
    actif = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Partenaire"
        verbose_name_plural = "Partenaires"
        ordering = ['ordre']
    
    def __str__(self):
        return self.nom
    
    panels = [
        FieldPanel('nom'),
        FieldPanel('logo'),
        FieldPanel('site_web'),
        FieldPanel('ordre'),
        FieldPanel('actif'),
    ]


@register_snippet
class ServiceMairie(models.Model):
    """Services proposés par la mairie."""
    nom = models.CharField(max_length=200, verbose_name="Nom du service")
    description = models.TextField(blank=True)
    icone = models.CharField(
        max_length=50, blank=True,
        help_text="Nom de l'icône (ex: users, file-text, calendar)"
    )
    lien_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="Page de détail"
    )
    ordre = models.PositiveIntegerField(default=0)
    actif = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Service de la mairie"
        verbose_name_plural = "Services de la mairie"
        ordering = ['ordre']
    
    def __str__(self):
        return self.nom
    
    panels = [
        FieldPanel('nom'),
        FieldPanel('description'),
        FieldPanel('icone'),
        PageChooserPanel('lien_page'),
        FieldPanel('ordre'),
        FieldPanel('actif'),
    ]


@register_snippet 
class MembreEquipe(models.Model):
    """Membres de l'équipe municipale."""
    nom = models.CharField(max_length=200)
    fonction = models.CharField(max_length=200)
    photo = models.ForeignKey(
        'cms.ImagePersonnalisee',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    biographie = RichTextField(blank=True)
    email = models.EmailField(blank=True)
    telephone = models.CharField(max_length=50, blank=True)
    ordre = models.PositiveIntegerField(default=0)
    actif = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Membre de l'équipe"
        verbose_name_plural = "Membres de l'équipe"
        ordering = ['ordre']
    
    def __str__(self):
        return f"{self.nom} - {self.fonction}"
    
    panels = [
        FieldPanel('nom'),
        FieldPanel('fonction'),
        FieldPanel('photo'),
        FieldPanel('biographie'),
        FieldPanel('email'),
        FieldPanel('telephone'),
        FieldPanel('ordre'),
        FieldPanel('actif'),
    ]


@register_snippet
class FAQ(models.Model):
    """Questions fréquemment posées."""
    question = models.CharField(max_length=500)
    reponse = RichTextField()
    categorie = models.CharField(max_length=100, blank=True)
    ordre = models.PositiveIntegerField(default=0)
    publie = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"
        ordering = ['categorie', 'ordre']
    
    def __str__(self):
        return self.question[:50]
    
    panels = [
        FieldPanel('question'),
        FieldPanel('reponse'),
        FieldPanel('categorie'),
        FieldPanel('ordre'),
        FieldPanel('publie'),
    ]


@register_snippet
class Temoignage(models.Model):
    """Témoignages de citoyens."""
    nom = models.CharField(max_length=200)
    fonction = models.CharField(max_length=200, blank=True)
    photo = models.ForeignKey(
        'cms.ImagePersonnalisee',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    temoignage = models.TextField()
    note = models.PositiveIntegerField(
        default=5,
        help_text="Note de 1 à 5"
    )
    publie = models.BooleanField(default=True)
    date = models.DateField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Témoignage"
        verbose_name_plural = "Témoignages"
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.nom} - {self.temoignage[:30]}..."
    
    panels = [
        FieldPanel('nom'),
        FieldPanel('fonction'),
        FieldPanel('photo'),
        FieldPanel('temoignage'),
        FieldPanel('note'),
        FieldPanel('publie'),
    ]


# =============================================================================
# PAGES WAGTAIL
# =============================================================================

class PageTag(TaggedItemBase):
    """Tags pour les pages."""
    content_object = ParentalKey(
        'cms.ArticlePage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )


class PageAccueil(Page):
    """Page d'accueil de la mairie."""
    
    # Hero section
    hero_titre = models.CharField(max_length=300, verbose_name="Titre du hero")
    hero_sous_titre = models.TextField(blank=True, verbose_name="Sous-titre")
    hero_image = models.ForeignKey(
        'cms.ImagePersonnalisee',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="Image de fond"
    )
    hero_bouton_texte = models.CharField(max_length=50, blank=True, default="Découvrir")
    hero_bouton_lien = models.ForeignKey(
        'wagtailcore.Page',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="Lien du bouton"
    )
    
    # Sections flexibles avec StreamField
    contenu = StreamField([
        ('hero', HeroBlock()),
        ('services', ServicesBlock()),
        ('actualites', CardsBlock()),
        ('statistiques', StatsBlock()),
        ('equipe', TeamBlock()),
        ('temoignages', TestimonialsBlock()),
        ('cta', CTABlock()),
        ('galerie', GalerieBlock()),
        ('texte_image', ImageTextBlock()),
        ('video', VideoBlock()),
        ('faq', AccordionBlock()),
        ('timeline', TimelineBlock()),
        ('contact', ContactBlock()),
        ('carte', MapBlock()),
        ('documents', DocumentsBlock()),
        ('texte_riche', RichTextBlock()),
    ], use_json_field=True, blank=True, verbose_name="Contenu de la page")
    
    # SEO
    seo_titre = models.CharField(max_length=70, blank=True, verbose_name="Titre SEO")
    seo_description = models.TextField(max_length=160, blank=True, verbose_name="Description SEO")
    
    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('hero_titre'),
            FieldPanel('hero_sous_titre'),
            FieldPanel('hero_image'),
            FieldPanel('hero_bouton_texte'),
            PageChooserPanel('hero_bouton_lien'),
        ], heading="Section Hero"),
        FieldPanel('contenu'),
    ]
    
    promote_panels = Page.promote_panels + [
        MultiFieldPanel([
            FieldPanel('seo_titre'),
            FieldPanel('seo_description'),
        ], heading="SEO"),
    ]
    
    search_fields = Page.search_fields + [
        index.SearchField('hero_titre'),
        index.SearchField('hero_sous_titre'),
    ]
    
    class Meta:
        verbose_name = "Page d'accueil"
    
    # Une seule page d'accueil par site
    max_count = 1
    parent_page_types = ['wagtailcore.Page']


class PageStandard(Page):
    """Page standard avec contenu flexible."""
    
    introduction = RichTextField(blank=True, verbose_name="Introduction")
    image_principale = models.ForeignKey(
        'cms.ImagePersonnalisee',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="Image principale"
    )
    
    contenu = StreamField([
        ('texte_riche', RichTextBlock()),
        ('texte_image', ImageTextBlock()),
        ('galerie', GalerieBlock()),
        ('video', VideoBlock()),
        ('accordion', AccordionBlock()),
        ('cta', CTABlock()),
        ('documents', DocumentsBlock()),
        ('contact', ContactBlock()),
        ('carte', MapBlock()),
        ('statistiques', StatsBlock()),
        ('equipe', TeamBlock()),
    ], use_json_field=True, blank=True)
    
    # SEO
    seo_titre = models.CharField(max_length=70, blank=True)
    seo_description = models.TextField(max_length=160, blank=True)
    
    content_panels = Page.content_panels + [
        FieldPanel('introduction'),
        FieldPanel('image_principale'),
        FieldPanel('contenu'),
    ]
    
    promote_panels = Page.promote_panels + [
        MultiFieldPanel([
            FieldPanel('seo_titre'),
            FieldPanel('seo_description'),
        ], heading="SEO"),
    ]
    
    search_fields = Page.search_fields + [
        index.SearchField('introduction'),
    ]
    
    class Meta:
        verbose_name = "Page standard"
        verbose_name_plural = "Pages standard"


class ArticleIndexPage(Page):
    """Page d'index des articles/actualités."""
    
    introduction = RichTextField(blank=True)
    
    content_panels = Page.content_panels + [
        FieldPanel('introduction'),
    ]
    
    def get_context(self, request):
        context = super().get_context(request)
        articles = ArticlePage.objects.live().descendant_of(self).order_by('-date_publication')
        
        # Filtrage par catégorie
        categorie = request.GET.get('categorie')
        if categorie:
            articles = articles.filter(categorie__slug=categorie)
        
        # Filtrage par tag
        tag = request.GET.get('tag')
        if tag:
            articles = articles.filter(tags__name=tag)
        
        context['articles'] = articles
        context['categories'] = CategorieArticle.objects.all()
        return context
    
    class Meta:
        verbose_name = "Index des articles"
    
    subpage_types = ['cms.ArticlePage']
    parent_page_types = ['cms.PageAccueil', 'cms.PageStandard']


@register_snippet
class CategorieArticle(models.Model):
    """Catégorie d'articles."""
    nom = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    icone = models.CharField(max_length=50, blank=True)
    couleur = models.CharField(max_length=7, default='#1E40AF')
    
    class Meta:
        verbose_name = "Catégorie d'article"
        verbose_name_plural = "Catégories d'articles"
        ordering = ['nom']
    
    def __str__(self):
        return self.nom
    
    panels = [
        FieldPanel('nom'),
        FieldPanel('slug'),
        FieldPanel('description'),
        FieldPanel('icone'),
        FieldPanel('couleur'),
    ]


class ArticlePage(Page):
    """Page article/actualité."""
    
    date_publication = models.DateField(verbose_name="Date de publication")
    auteur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='articles_wagtail'
    )
    categorie = models.ForeignKey(
        CategorieArticle,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='articles'
    )
    tags = ClusterTaggableManager(through=PageTag, blank=True)
    
    image_principale = models.ForeignKey(
        'cms.ImagePersonnalisee',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="Image principale"
    )
    
    resume = models.TextField(max_length=500, verbose_name="Résumé")
    
    contenu = StreamField([
        ('texte_riche', RichTextBlock()),
        ('texte_image', ImageTextBlock()),
        ('galerie', GalerieBlock()),
        ('video', VideoBlock()),
        ('citation', RichTextBlock()),
        ('documents', DocumentsBlock()),
    ], use_json_field=True)
    
    # Statistiques
    vues = models.PositiveIntegerField(default=0)
    
    # SEO
    seo_titre = models.CharField(max_length=70, blank=True)
    seo_description = models.TextField(max_length=160, blank=True)
    
    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('date_publication'),
                FieldPanel('auteur'),
            ]),
            FieldPanel('categorie'),
            FieldPanel('tags'),
        ], heading="Métadonnées"),
        FieldPanel('image_principale'),
        FieldPanel('resume'),
        FieldPanel('contenu'),
    ]
    
    promote_panels = Page.promote_panels + [
        MultiFieldPanel([
            FieldPanel('seo_titre'),
            FieldPanel('seo_description'),
        ], heading="SEO"),
    ]
    
    search_fields = Page.search_fields + [
        index.SearchField('resume'),
        index.FilterField('date_publication'),
        index.FilterField('categorie'),
    ]
    
    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"
        ordering = ['-date_publication']
    
    parent_page_types = ['cms.ArticleIndexPage']


class EvenementIndexPage(Page):
    """Page d'index des événements."""
    
    introduction = RichTextField(blank=True)
    
    content_panels = Page.content_panels + [
        FieldPanel('introduction'),
    ]
    
    def get_context(self, request):
        context = super().get_context(request)
        from django.utils import timezone
        
        evenements = EvenementPage.objects.live().descendant_of(self)
        
        # Filtrer: à venir ou passés
        filtre = request.GET.get('filtre', 'avenir')
        if filtre == 'avenir':
            evenements = evenements.filter(date_debut__gte=timezone.now()).order_by('date_debut')
        else:
            evenements = evenements.filter(date_debut__lt=timezone.now()).order_by('-date_debut')
        
        context['evenements'] = evenements
        context['filtre_actif'] = filtre
        return context
    
    class Meta:
        verbose_name = "Index des événements"
    
    subpage_types = ['cms.EvenementPage']


class EvenementPage(Page):
    """Page événement."""
    
    date_debut = models.DateTimeField(verbose_name="Date de début")
    date_fin = models.DateTimeField(null=True, blank=True, verbose_name="Date de fin")
    
    lieu = models.CharField(max_length=300)
    adresse = models.TextField(blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    
    image_principale = models.ForeignKey(
        'cms.ImagePersonnalisee',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    
    description = RichTextField()
    
    organisateur = models.CharField(max_length=200, blank=True)
    contact_email = models.EmailField(blank=True)
    contact_telephone = models.CharField(max_length=50, blank=True)
    
    gratuit = models.BooleanField(default=True)
    prix = models.CharField(max_length=100, blank=True)
    lien_inscription = models.URLField(blank=True)
    
    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('date_debut'),
                FieldPanel('date_fin'),
            ]),
        ], heading="Dates"),
        MultiFieldPanel([
            FieldPanel('lieu'),
            FieldPanel('adresse'),
            FieldRowPanel([
                FieldPanel('latitude'),
                FieldPanel('longitude'),
            ]),
        ], heading="Lieu"),
        FieldPanel('image_principale'),
        FieldPanel('description'),
        MultiFieldPanel([
            FieldPanel('organisateur'),
            FieldPanel('contact_email'),
            FieldPanel('contact_telephone'),
        ], heading="Contact"),
        MultiFieldPanel([
            FieldPanel('gratuit'),
            FieldPanel('prix'),
            FieldPanel('lien_inscription'),
        ], heading="Tarification"),
    ]
    
    search_fields = Page.search_fields + [
        index.SearchField('lieu'),
        index.SearchField('description'),
        index.FilterField('date_debut'),
    ]
    
    class Meta:
        verbose_name = "Événement"
        verbose_name_plural = "Événements"
    
    parent_page_types = ['cms.EvenementIndexPage']


class ServicePage(Page):
    """Page de service municipal."""
    
    icone = models.CharField(max_length=50, blank=True)
    image_principale = models.ForeignKey(
        'cms.ImagePersonnalisee',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    
    introduction = RichTextField()
    
    contenu = StreamField([
        ('texte_riche', RichTextBlock()),
        ('texte_image', ImageTextBlock()),
        ('accordion', AccordionBlock()),
        ('documents', DocumentsBlock()),
        ('contact', ContactBlock()),
        ('cta', CTABlock()),
    ], use_json_field=True, blank=True)
    
    # Informations pratiques
    horaires = RichTextField(blank=True)
    lieu = models.CharField(max_length=300, blank=True)
    contact_email = models.EmailField(blank=True)
    contact_telephone = models.CharField(max_length=50, blank=True)
    
    # Documents à télécharger
    documents_requis = RichTextField(blank=True, verbose_name="Documents requis")
    
    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('icone'),
            FieldPanel('image_principale'),
        ], heading="Visuel"),
        FieldPanel('introduction'),
        FieldPanel('contenu'),
        MultiFieldPanel([
            FieldPanel('horaires'),
            FieldPanel('lieu'),
            FieldPanel('contact_email'),
            FieldPanel('contact_telephone'),
        ], heading="Informations pratiques"),
        FieldPanel('documents_requis'),
    ]
    
    search_fields = Page.search_fields + [
        index.SearchField('introduction'),
    ]
    
    class Meta:
        verbose_name = "Page service"
        verbose_name_plural = "Pages services"


class EquipePage(Page):
    """Page de l'équipe municipale."""
    
    introduction = RichTextField(blank=True)
    image_principale = models.ForeignKey(
        'cms.ImagePersonnalisee',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    
    contenu = StreamField([
        ('texte_riche', RichTextBlock()),
        ('equipe', TeamBlock()),
    ], use_json_field=True, blank=True)
    
    content_panels = Page.content_panels + [
        FieldPanel('introduction'),
        FieldPanel('image_principale'),
        FieldPanel('contenu'),
    ]
    
    class Meta:
        verbose_name = "Page équipe"
    
    max_count = 1


class ContactPage(Page):
    """Page de contact."""
    
    introduction = RichTextField(blank=True)
    
    # Coordonnées principales
    adresse = models.TextField(blank=True)
    email = models.EmailField(blank=True)
    telephone = models.CharField(max_length=50, blank=True)
    
    # Carte
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    
    # Horaires
    horaires = RichTextField(blank=True)
    
    # Message de confirmation
    message_confirmation = models.TextField(
        default="Votre message a bien été envoyé. Nous vous répondrons dans les plus brefs délais."
    )
    
    contenu = StreamField([
        ('texte_riche', RichTextBlock()),
        ('contact', ContactBlock()),
        ('carte', MapBlock()),
    ], use_json_field=True, blank=True)
    
    content_panels = Page.content_panels + [
        FieldPanel('introduction'),
        MultiFieldPanel([
            FieldPanel('adresse'),
            FieldPanel('email'),
            FieldPanel('telephone'),
        ], heading="Coordonnées"),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('latitude'),
                FieldPanel('longitude'),
            ]),
        ], heading="Carte"),
        FieldPanel('horaires'),
        FieldPanel('message_confirmation'),
        FieldPanel('contenu'),
    ]
    
    class Meta:
        verbose_name = "Page contact"
    
    max_count = 1


# =============================================================================
# FORMULAIRES WAGTAIL
# =============================================================================

class ChampFormulaire(AbstractFormField):
    """Champ de formulaire personnalisé."""
    page = ParentalKey(
        'FormulaireContactPage',
        on_delete=models.CASCADE,
        related_name='form_fields'
    )


class FormulaireContactPage(AbstractEmailForm):
    """Page formulaire de contact."""
    
    introduction = RichTextField(blank=True)
    remerciement = RichTextField(blank=True, verbose_name="Message de remerciement")
    
    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel('introduction'),
        InlinePanel('form_fields', label="Champs du formulaire"),
        FieldPanel('remerciement'),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('to_address'),
                FieldPanel('from_address'),
            ]),
            FieldPanel('subject'),
        ], heading="Configuration email"),
    ]
    
    class Meta:
        verbose_name = "Formulaire de contact"


class ProjetIndexPage(Page):
    """Page d'index des projets municipaux."""
    
    introduction = RichTextField(blank=True)
    
    content_panels = Page.content_panels + [
        FieldPanel('introduction'),
    ]
    
    def get_context(self, request):
        context = super().get_context(request)
        projets = ProjetPage.objects.live().descendant_of(self).order_by('-first_published_at')
        
        # Filtrage par statut
        statut = request.GET.get('statut')
        if statut:
            projets = projets.filter(statut=statut)
        
        context['projets'] = projets
        return context
    
    class Meta:
        verbose_name = "Index des projets"
    
    subpage_types = ['cms.ProjetPage']


class ProjetPage(Page):
    """Page de projet municipal."""
    
    STATUT_CHOICES = [
        ('planifie', 'Planifié'),
        ('en_cours', 'En cours'),
        ('suspendu', 'Suspendu'),
        ('termine', 'Terminé'),
        ('annule', 'Annulé'),
    ]
    
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='planifie')
    pourcentage_avancement = models.PositiveIntegerField(default=0)
    
    image_principale = models.ForeignKey(
        'cms.ImagePersonnalisee',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    
    description = RichTextField()
    objectifs = RichTextField(blank=True)
    
    budget_alloue = models.DecimalField(max_digits=15, decimal_places=0, null=True, blank=True)
    budget_execute = models.DecimalField(max_digits=15, decimal_places=0, null=True, blank=True)
    
    date_debut = models.DateField(null=True, blank=True)
    date_fin_prevue = models.DateField(null=True, blank=True)
    date_fin_reelle = models.DateField(null=True, blank=True)
    
    responsable = models.CharField(max_length=200, blank=True)
    partenaires = models.TextField(blank=True)
    
    contenu = StreamField([
        ('texte_riche', RichTextBlock()),
        ('texte_image', ImageTextBlock()),
        ('galerie', GalerieBlock()),
        ('video', VideoBlock()),
        ('timeline', TimelineBlock()),
        ('documents', DocumentsBlock()),
    ], use_json_field=True, blank=True)
    
    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('statut'),
                FieldPanel('pourcentage_avancement'),
            ]),
        ], heading="Statut"),
        FieldPanel('image_principale'),
        FieldPanel('description'),
        FieldPanel('objectifs'),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('budget_alloue'),
                FieldPanel('budget_execute'),
            ]),
        ], heading="Budget"),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('date_debut'),
                FieldPanel('date_fin_prevue'),
            ]),
            FieldPanel('date_fin_reelle'),
        ], heading="Dates"),
        MultiFieldPanel([
            FieldPanel('responsable'),
            FieldPanel('partenaires'),
        ], heading="Responsables"),
        FieldPanel('contenu'),
    ]
    
    search_fields = Page.search_fields + [
        index.SearchField('description'),
        index.FilterField('statut'),
    ]
    
    class Meta:
        verbose_name = "Projet municipal"
        verbose_name_plural = "Projets municipaux"
    
    parent_page_types = ['cms.ProjetIndexPage']
    
    @property
    def taux_execution(self):
        if self.budget_alloue and self.budget_execute:
            return round((float(self.budget_execute) / float(self.budget_alloue)) * 100, 1)
        return 0
