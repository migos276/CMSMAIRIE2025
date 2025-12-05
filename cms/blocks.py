"""
Blocs StreamField pour Wagtail.
Composants réutilisables pour les pages.
"""
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.snippets.blocks import SnippetChooserBlock
from wagtail.embeds.blocks import EmbedBlock


class LinkBlock(blocks.StructBlock):
    """Bloc de lien."""
    texte = blocks.CharBlock(required=True)
    page = blocks.PageChooserBlock(required=False)
    url_externe = blocks.URLBlock(required=False)
    
    class Meta:
        icon = 'link'
        label = 'Lien'


class BoutonBlock(blocks.StructBlock):
    """Bloc de bouton avec variantes."""
    texte = blocks.CharBlock(required=True)
    page = blocks.PageChooserBlock(required=False)
    url_externe = blocks.URLBlock(required=False)
    style = blocks.ChoiceBlock(choices=[
        ('primary', 'Primaire'),
        ('secondary', 'Secondaire'),
        ('outline', 'Contour'),
        ('ghost', 'Transparent'),
    ], default='primary')
    
    class Meta:
        icon = 'placeholder'
        label = 'Bouton'


class HeroBlock(blocks.StructBlock):
    """Bloc hero/bannière principale."""
    titre = blocks.CharBlock(required=True, max_length=200)
    sous_titre = blocks.TextBlock(required=False)
    image = ImageChooserBlock(required=False)
    video_url = blocks.URLBlock(required=False, help_text="URL YouTube ou Vimeo")
    overlay = blocks.BooleanBlock(required=False, default=True, help_text="Ajouter un overlay sombre")
    boutons = blocks.ListBlock(BoutonBlock(), max_num=2)
    hauteur = blocks.ChoiceBlock(choices=[
        ('small', 'Petite (400px)'),
        ('medium', 'Moyenne (500px)'),
        ('large', 'Grande (600px)'),
        ('full', 'Plein écran'),
    ], default='large')
    
    class Meta:
        icon = 'image'
        label = 'Hero / Bannière'
        template = 'cms/blocks/hero.html'


class CardBlock(blocks.StructBlock):
    """Bloc carte individuelle."""
    titre = blocks.CharBlock(required=True)
    description = blocks.TextBlock(required=False)
    image = ImageChooserBlock(required=False)
    lien = blocks.PageChooserBlock(required=False)
    url_externe = blocks.URLBlock(required=False)
    icone = blocks.CharBlock(required=False, help_text="Nom de l'icône")
    
    class Meta:
        icon = 'doc-full'
        label = 'Carte'


class CardsBlock(blocks.StructBlock):
    """Bloc grille de cartes."""
    titre_section = blocks.CharBlock(required=False)
    sous_titre = blocks.TextBlock(required=False)
    cartes = blocks.ListBlock(CardBlock())
    colonnes = blocks.ChoiceBlock(choices=[
        ('2', '2 colonnes'),
        ('3', '3 colonnes'),
        ('4', '4 colonnes'),
    ], default='3')
    
    class Meta:
        icon = 'grip'
        label = 'Grille de cartes'
        template = 'cms/blocks/cards.html'


class CTABlock(blocks.StructBlock):
    """Bloc appel à l'action."""
    titre = blocks.CharBlock(required=True)
    description = blocks.TextBlock(required=False)
    image_fond = ImageChooserBlock(required=False)
    bouton = BoutonBlock()
    style = blocks.ChoiceBlock(choices=[
        ('light', 'Clair'),
        ('dark', 'Sombre'),
        ('primary', 'Couleur primaire'),
        ('gradient', 'Dégradé'),
    ], default='primary')
    
    class Meta:
        icon = 'pick'
        label = 'Appel à l\'action'
        template = 'cms/blocks/cta.html'


class GalerieImageBlock(blocks.StructBlock):
    """Image de galerie."""
    image = ImageChooserBlock(required=True)
    legende = blocks.CharBlock(required=False)


class GalerieBlock(blocks.StructBlock):
    """Bloc galerie d'images."""
    titre = blocks.CharBlock(required=False)
    images = blocks.ListBlock(GalerieImageBlock())
    colonnes = blocks.ChoiceBlock(choices=[
        ('2', '2 colonnes'),
        ('3', '3 colonnes'),
        ('4', '4 colonnes'),
    ], default='3')
    lightbox = blocks.BooleanBlock(required=False, default=True)
    
    class Meta:
        icon = 'image'
        label = 'Galerie'
        template = 'cms/blocks/galerie.html'


class AccordionItemBlock(blocks.StructBlock):
    """Élément d'accordéon."""
    titre = blocks.CharBlock(required=True)
    contenu = blocks.RichTextBlock(required=True)
    ouvert = blocks.BooleanBlock(required=False, default=False)


class AccordionBlock(blocks.StructBlock):
    """Bloc accordéon/FAQ."""
    titre_section = blocks.CharBlock(required=False)
    elements = blocks.ListBlock(AccordionItemBlock())
    
    class Meta:
        icon = 'list-ul'
        label = 'Accordéon / FAQ'
        template = 'cms/blocks/accordion.html'


class TimelineItemBlock(blocks.StructBlock):
    """Élément de timeline."""
    date = blocks.CharBlock(required=True)
    titre = blocks.CharBlock(required=True)
    description = blocks.TextBlock(required=False)
    image = ImageChooserBlock(required=False)


class TimelineBlock(blocks.StructBlock):
    """Bloc timeline/chronologie."""
    titre_section = blocks.CharBlock(required=False)
    elements = blocks.ListBlock(TimelineItemBlock())
    
    class Meta:
        icon = 'time'
        label = 'Chronologie'
        template = 'cms/blocks/timeline.html'


class StatBlock(blocks.StructBlock):
    """Statistique individuelle."""
    valeur = blocks.CharBlock(required=True, help_text="Ex: 10000, 95%")
    label = blocks.CharBlock(required=True)
    icone = blocks.CharBlock(required=False)
    description = blocks.TextBlock(required=False)


class StatsBlock(blocks.StructBlock):
    """Bloc statistiques."""
    titre_section = blocks.CharBlock(required=False)
    sous_titre = blocks.TextBlock(required=False)
    statistiques = blocks.ListBlock(StatBlock())
    style = blocks.ChoiceBlock(choices=[
        ('light', 'Fond clair'),
        ('dark', 'Fond sombre'),
        ('primary', 'Fond primaire'),
    ], default='light')
    
    class Meta:
        icon = 'order'
        label = 'Statistiques'
        template = 'cms/blocks/stats.html'


class TeamMemberBlock(blocks.StructBlock):
    """Membre d'équipe."""
    membre = SnippetChooserBlock('cms.MembreEquipe')


class TeamBlock(blocks.StructBlock):
    """Bloc équipe."""
    titre_section = blocks.CharBlock(required=False)
    sous_titre = blocks.TextBlock(required=False)
    membres = blocks.ListBlock(TeamMemberBlock())
    colonnes = blocks.ChoiceBlock(choices=[
        ('3', '3 colonnes'),
        ('4', '4 colonnes'),
    ], default='4')
    
    class Meta:
        icon = 'group'
        label = 'Équipe'
        template = 'cms/blocks/team.html'


class TemoignageItemBlock(blocks.StructBlock):
    """Témoignage individuel."""
    temoignage = SnippetChooserBlock('cms.Temoignage')


class TestimonialsBlock(blocks.StructBlock):
    """Bloc témoignages."""
    titre_section = blocks.CharBlock(required=False)
    temoignages = blocks.ListBlock(TemoignageItemBlock())
    carrousel = blocks.BooleanBlock(required=False, default=True)
    
    class Meta:
        icon = 'openquote'
        label = 'Témoignages'
        template = 'cms/blocks/testimonials.html'


class ContactBlock(blocks.StructBlock):
    """Bloc informations de contact."""
    titre = blocks.CharBlock(required=False, default="Nous contacter")
    adresse = blocks.TextBlock(required=False)
    telephone = blocks.CharBlock(required=False)
    email = blocks.EmailBlock(required=False)
    horaires = blocks.RichTextBlock(required=False)
    afficher_formulaire = blocks.BooleanBlock(required=False, default=False)
    
    class Meta:
        icon = 'mail'
        label = 'Contact'
        template = 'cms/blocks/contact.html'


class MapBlock(blocks.StructBlock):
    """Bloc carte/map."""
    titre = blocks.CharBlock(required=False)
    latitude = blocks.FloatBlock(required=True)
    longitude = blocks.FloatBlock(required=True)
    zoom = blocks.IntegerBlock(default=15, min_value=1, max_value=20)
    hauteur = blocks.IntegerBlock(default=400, help_text="Hauteur en pixels")
    marqueur_titre = blocks.CharBlock(required=False)
    
    class Meta:
        icon = 'site'
        label = 'Carte'
        template = 'cms/blocks/map.html'


class ServiceItemBlock(blocks.StructBlock):
    """Service individuel."""
    service = SnippetChooserBlock('cms.ServiceMairie')


class ServicesBlock(blocks.StructBlock):
    """Bloc services."""
    titre_section = blocks.CharBlock(required=False)
    sous_titre = blocks.TextBlock(required=False)
    services = blocks.ListBlock(ServiceItemBlock())
    colonnes = blocks.ChoiceBlock(choices=[
        ('2', '2 colonnes'),
        ('3', '3 colonnes'),
        ('4', '4 colonnes'),
    ], default='3')
    
    class Meta:
        icon = 'cogs'
        label = 'Services'
        template = 'cms/blocks/services.html'


class RichTextBlock(blocks.StructBlock):
    """Bloc texte riche."""
    contenu = blocks.RichTextBlock()
    colonnes = blocks.ChoiceBlock(choices=[
        ('1', '1 colonne (pleine largeur)'),
        ('2', '2 colonnes'),
    ], default='1')
    
    class Meta:
        icon = 'doc-full'
        label = 'Texte riche'
        template = 'cms/blocks/richtext.html'


class ImageTextBlock(blocks.StructBlock):
    """Bloc image + texte."""
    image = ImageChooserBlock(required=True)
    titre = blocks.CharBlock(required=False)
    texte = blocks.RichTextBlock()
    position_image = blocks.ChoiceBlock(choices=[
        ('left', 'Image à gauche'),
        ('right', 'Image à droite'),
    ], default='left')
    ratio = blocks.ChoiceBlock(choices=[
        ('50-50', '50% - 50%'),
        ('40-60', '40% - 60%'),
        ('60-40', '60% - 40%'),
    ], default='50-50')
    
    class Meta:
        icon = 'image'
        label = 'Image + Texte'
        template = 'cms/blocks/image_text.html'


class VideoBlock(blocks.StructBlock):
    """Bloc vidéo."""
    titre = blocks.CharBlock(required=False)
    video = EmbedBlock()
    description = blocks.TextBlock(required=False)
    
    class Meta:
        icon = 'media'
        label = 'Vidéo'
        template = 'cms/blocks/video.html'


class DocumentItemBlock(blocks.StructBlock):
    """Document individuel."""
    document = DocumentChooserBlock(required=True)
    titre_personnalise = blocks.CharBlock(required=False)
    description = blocks.TextBlock(required=False)


class DocumentsBlock(blocks.StructBlock):
    """Bloc liste de documents."""
    titre = blocks.CharBlock(required=False)
    documents = blocks.ListBlock(DocumentItemBlock())
    affichage = blocks.ChoiceBlock(choices=[
        ('liste', 'Liste'),
        ('grille', 'Grille'),
        ('tableau', 'Tableau'),
    ], default='liste')
    
    class Meta:
        icon = 'doc-full-inverse'
        label = 'Documents'
        template = 'cms/blocks/documents.html'
