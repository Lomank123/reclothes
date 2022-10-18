from accounts.views import AccountsLoginView
from carts.urls import router as carts_router
from catalogue.urls import router as catalogue_router
from orders.urls import router as orders_router
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from accounts.urls import api_urlpatterns as accounts_api


# Main API router
router = DefaultRouter()
router.registry.extend(catalogue_router.registry)
router.registry.extend(carts_router.registry)
router.registry.extend(orders_router.registry)

# TODO: Replace router with this
api_urlpatterns = [
    path('user/', include((accounts_api, 'user'), namespace='user')),
]

urlpatterns = [
    # Admin
    path('lomank/login/', AccountsLoginView.as_view(), name='login'),
    path('lomank/', admin.site.urls),

    # API
    path('api/', include(router.urls)),

    # App urls
    path('', include(('catalogue.urls', 'catalogue'), namespace='catalogue')),
    path('auth/', include(
        ('accounts.urls', 'accounts'), namespace='accounts')),
    path('cart/', include(('carts.urls', 'carts'), namespace='carts')),
    path('order/', include(('orders.urls', 'orders'), namespace='orders')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT)
