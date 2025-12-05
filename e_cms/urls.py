"""
URL configuration for E-CMS project with Wagtail.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from wagtail.api.v2.views import PagesAPIViewSet
from wagtail.api.v2.router import WagtailAPIRouter
from wagtail.images.api.v2.views import ImagesAPIViewSet
from wagtail.documents.api.v2.views import DocumentsAPIViewSet

api_router = WagtailAPIRouter('wagtailapi')
api_router.register_endpoint('pages', PagesAPIViewSet)
api_router.register_endpoint('images', ImagesAPIViewSet)
api_router.register_endpoint('documents', DocumentsAPIViewSet)

urlpatterns = [
    # Django admin
    path('admin/', admin.site.urls),
    
    path('cms-admin/', include(wagtailadmin_urls)),
    
    path('documents/', include(wagtaildocs_urls)),
    
    path('api/v2/', api_router.urls),
    
    # E-CMS apps
    path('', include('core.urls')),
    path('etat-civil/', include('etat_civil.urls')),
    path('contenu/', include('contenu.urls')),
    path('services/', include('services.urls')),
    path('utilisateurs/', include('utilisateurs.urls')),
    
    path('', include(wagtail_urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
