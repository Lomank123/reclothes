from accounts.urls import router as accounts_router
from accounts.views import AccountsLoginView
from carts.urls import router as carts_router
from catalogue.urls import router as catalogue_router
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter


# Main API router
router = DefaultRouter()
router.registry.extend(catalogue_router.registry)
router.registry.extend(accounts_router.registry)
router.registry.extend(carts_router.registry)

urlpatterns = [
    path('lomank/login/', AccountsLoginView.as_view(), name='login'),
    path('lomank/', admin.site.urls),
    path('api/', include(router.urls)),
    path('', include(('catalogue.urls', 'catalogue'), namespace='catalogue')),
    path('auth/', include(('accounts.urls', 'accounts'), namespace='accounts')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
