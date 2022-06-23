from django.urls import path
from rest_framework.routers import DefaultRouter

from accounts import views, viewsets


router = DefaultRouter()
router.register("user", viewsets.CustomUserViewSet, basename="user")

urlpatterns = [
    path('login/', views.AccountsLoginView.as_view(), name='login'),
    path('logout/', views.AccountsLogoutView.as_view(), name='logout'),
    path('signup/', views.AccountsSignupView.as_view(), name='signup'),
]
