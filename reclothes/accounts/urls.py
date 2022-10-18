from django.urls import path

from accounts.views import (AccountsLoginView, AccountsLogoutView,
                            AccountsSignupView, CustomUserDetailView,
                            CustomUserProfileView)


# 2-tuple contains list of patterns and app namespace
api_urlpatterns = ([
    path('<int:pk>/', CustomUserDetailView.as_view(), name='detail'),
], 'user')

urlpatterns = [
    path('login/', AccountsLoginView.as_view(), name='login'),
    path('logout/', AccountsLogoutView.as_view(), name='logout'),
    path('signup/', AccountsSignupView.as_view(), name='signup'),
    path('profile/', CustomUserProfileView.as_view(), name='profile'),
]
