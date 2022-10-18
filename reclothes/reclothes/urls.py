from accounts.urls import api_urlpatterns as accounts_api
from accounts.views import AccountsLoginView
from carts.urls import api_urlpatterns as carts_api
from catalogue.urls import router as catalogue_router
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from orders.urls import router as orders_router
from rest_framework.routers import DefaultRouter


# TODO: Remove this
# Main API router
router = DefaultRouter()
router.registry.extend(catalogue_router.registry)
router.registry.extend(orders_router.registry)

api_urlpatterns = [
    path('user/', include(accounts_api, namespace='user-api')),
    path('cart/', include(carts_api, namespace='cart-api')),
]

urlpatterns = [
    # Admin
    path('lomank/login/', AccountsLoginView.as_view(), name='login'),
    path('lomank/', admin.site.urls),

    # API
    path('api/', include((api_urlpatterns, 'api'), namespace='api')),

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
