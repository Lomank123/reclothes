from django.urls import path
from catalogue import views


product_api = ([
    path('', views.ProductListAPIView.as_view(), name='product-list'),
    path(
        '<int:pk>/',
        views.ProductDetailAPIView.as_view(),
        name='product-detail',
    ),
    path('home/', views.HomeListAPIView.as_view(), name='home-list'),
], 'catalogue')

category_api = ([
    path('', views.CategoryListAPIView.as_view(), name='category-list'),
    path(
        '<int:pk>/',
        views.CategoryDetailAPIView.as_view(),
        name='category-detail',
    ),
], 'catalogue')

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path(
        'product/<int:pk>/',
        views.ProductDetailView.as_view(),
        name='product-detail',
    ),
    path('catalogue/', views.CatalogueView.as_view(), name='catalogue'),
    path('categories/', views.CategoriesView.as_view(), name='categories'),
]
