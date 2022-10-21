from django.urls import path

from carts.views import (CartItemDetailAPIView, CartItemListAPIView, CartView,
                         CurrentCartAPIView)

api_urlpatterns = ([
    path('current/', CurrentCartAPIView.as_view(), name='current'),
    path('items/', CartItemListAPIView.as_view(), name='items-list'),
    path('items/<int:pk>/', CartItemDetailAPIView.as_view(), name='items-detail'),
], 'cart')

urlpatterns = [
    path('', CartView.as_view(), name='cart'),
]
