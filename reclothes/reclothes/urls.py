from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework.routers import DefaultRouter

from catalogue.urls import router as catalogue_router
from accounts.urls import router as accounts_router


# Main API router
router = DefaultRouter()
router.registry.extend(catalogue_router.registry)
router.registry.extend(accounts_router.registry)

urlpatterns = [
    path('lomank/', admin.site.urls),
    path('api/', include(router.urls)),
    path('', include(('catalogue.urls', 'catalogue'), namespace='catalogue')),
    path('auth/', include(('accounts.urls', 'accounts'), namespace='accounts')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
