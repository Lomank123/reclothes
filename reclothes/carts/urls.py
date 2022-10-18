from django.urls import path

from carts.views import (CartItemDetailView, CartItemListView, CartView,
                         CurrentCartView)

api_urlpatterns = ([
    path('current/', CurrentCartView.as_view(), name='current'),
    path('items/', CartItemListView.as_view(), name='items-list'),
    path('items/<int:pk>/', CartItemDetailView.as_view(), name='items-detail'),
], 'cart')

urlpatterns = [
    path('', CartView.as_view(), name='cart'),
]
