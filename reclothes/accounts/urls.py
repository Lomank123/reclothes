from django.urls import path
from rest_framework.routers import DefaultRouter

from accounts.views import (AccountsLoginView, AccountsLogoutView,
                            AccountsSignupView, UserProfileView)
from accounts.viewsets import CustomUserViewSet


router = DefaultRouter()
router.register("user", CustomUserViewSet, basename="user")

urlpatterns = [
    path('login/', AccountsLoginView.as_view(), name='login'),
    path('logout/', AccountsLogoutView.as_view(), name='logout'),
    path('signup/', AccountsSignupView.as_view(), name='signup'),
    path('profile/', UserProfileView.as_view(), name='profile'),
]
