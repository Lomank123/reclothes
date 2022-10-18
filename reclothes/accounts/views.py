from carts.services import CartToSessionService
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.forms import CustomUserCreationForm
from accounts.models import CustomUser
from accounts.serializers import CustomUserDetailSerializer


class AccountsLoginView(LoginView):
    template_name = 'accounts/login.html'

    def form_valid(self, form):
        login(self.request, form.get_user())
        # Update cart id in session
        CartToSessionService(self.request).execute()
        return HttpResponseRedirect(self.get_success_url())


class AccountsLogoutView(LogoutView):
    template_name = 'accounts/logout.html'
    next_page = '/'


class AccountsSignupView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'accounts/signup.html'
    success_url = '/'

    def form_valid(self, form):
        valid = super().form_valid(form)
        raw_password = form.cleaned_data.get('password1')
        email = form.cleaned_data.get('email')
        user = authenticate(username=email, password=raw_password)
        login(self.request, user)
        return valid


class CustomUserProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'


class CustomUserDetailView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, pk):
        user = CustomUser.objects.filter(id=pk).first()
        serializer = CustomUserDetailSerializer(user)
        return Response(data=serializer.data)
