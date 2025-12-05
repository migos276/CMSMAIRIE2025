"""Django management command to provision a tenant/site from a simple template.

Usage:
  python manage.py create_site_from_template --code=code --domain=domain [--name="Mairie"]

This command will:
 - create a `Mairie` tenant if it does not exist
 - create a `Domaine` for that tenant
 - if using django-tenants (Postgres), it will switch to the tenant schema and create a minimal Wagtail site structure
 - if using SQLite (no tenants), it will create the pages in the default schema

This is a conservative initial implementation: it will create a root page and a homepage with a title.
Further cloning of snippets and media can be added later.
"""
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
import sys

from tenants.models import Mairie, Domaine


class Command(BaseCommand):
    help = 'Create a tenant/site from a minimal template'

    def add_arguments(self, parser):
        parser.add_argument('--code', required=True, help='Unique code for the mairie (schema_name)')
        parser.add_argument('--domain', required=True, help='Domain name for the tenant (ex: mairie-xxx.localhost)')
        parser.add_argument('--name', required=False, default=None, help='Display name for the mairie')

    def handle(self, *args, **options):
        code = options['code']
        domain = options['domain']
        name = options.get('name') or f'Mairie {code}'

        # Create or get Mairie
        mairie, created = Mairie.objects.get_or_create(
            code=code,
            defaults={
                'nom': name,
                'code': code,
                'region': 'Non renseignée',
                'departement': 'Non renseigné',
                'arrondissement': 'Non renseigné',
                'adresse': '',
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS(f'Created tenant Mairie: {mairie}'))
        else:
            self.stdout.write(self.style.WARNING(f'Mairie already exists: {mairie}'))

        # Create domain
        domaine_obj, dcreated = Domaine.objects.get_or_create(
            domain=domain,
            tenant=mairie,
            defaults={'is_primary': True}
        )

        if dcreated:
            self.stdout.write(self.style.SUCCESS(f'Created domain: {domain}'))
        else:
            self.stdout.write(self.style.WARNING(f'Domain already exists: {domain}'))

        # Now provision Wagtail pages inside tenant schema if django-tenants is active
        use_sqlite = getattr(settings, 'USE_SQLITE', False)

        try:
            if not use_sqlite:
                # Defer import until runtime
                from django_tenants.utils import schema_context
                with schema_context(mairie.schema_name):
                    self._create_minimal_wagtail_site()
            else:
                # SQLite / single schema
                self._create_minimal_wagtail_site()

            self.stdout.write(self.style.SUCCESS('Provisioning completed.'))
            self.stdout.write('You can now visit the Wagtail admin at /cms-admin/ for this site (if running).')

        except Exception as e:
            raise CommandError(f'Error while provisioning site: {e}')

    def _create_minimal_wagtail_site(self):
        """Create a root page and a basic home page if they do not exist.

        This function imports Wagtail models at runtime to avoid import errors when Wagtail isn't installed.
        """
        try:
            from wagtail.models import Page, Site
            from cms.models import ConfigurationMairie
        except Exception as e:
            raise CommandError('Wagtail does not seem to be installed/configured: %s' % e)

        # Ensure there is a root (wagtail creates a root page automatically in most installs)
        root = Page.get_first_root_node()

        # Check for an existing HomePage (search by slug 'home' or title)
        existing = Page.objects.filter(slug='home').first()
        if existing:
            self.stdout.write(self.style.NOTICE('Home page already exists; skipping page creation.'))
            # Ensure a Site entry points to this root
            self._ensure_site(root_path=existing.get_path(), root_page=existing)
            return

        # Create a minimal generic page as home if a custom HomePage model isn't present
        home_page = Page(
            title='Accueil',
            slug='home'
        )
        root.add_child(instance=home_page)
        home_page.save_revision().publish()

        self.stdout.write(self.style.SUCCESS('Created basic Home page (title=Accueil, slug=home)'))

        # Create a Site record pointing to home
        self._ensure_site(root_path=home_page.get_path(), root_page=home_page)

        # Create default ConfigurationMairie settings if model exists
        try:
            conf, ccreated = ConfigurationMairie.objects.get_or_create(
                # there's normally one settings instance per site; wagtail's settings are per site, but the model is BaseSiteSetting
                defaults={'nom_mairie': 'Mairie', 'slogan': ''}
            )
            if ccreated:
                self.stdout.write(self.style.SUCCESS('Created default ConfigurationMairie.'))
        except Exception:
            # Model might not be present or migrations not applied; ignore safely
            pass

    def _ensure_site(self, root_path, root_page):
        from wagtail.models import Site

        # Try to get existing Site for this hostname; if none, create a generic one
        site_qs = Site.objects.all()
        if site_qs.exists():
            self.stdout.write(self.style.NOTICE('A Wagtail Site already exists; not creating a new Site record.'))
            return

        site = Site(hostname='localhost', root_page=root_page, is_default_site=True)
        site.save()
        self.stdout.write(self.style.SUCCESS('Created Wagtail Site (hostname=localhost, is_default_site=True)'))
