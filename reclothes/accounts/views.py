from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView

from accounts.forms import CustomUserCreationForm
from accounts.models import CustomUser
from accounts.services import LoginViewService


class AccountsLoginView(LoginView):
    template_name = 'accounts/login.html'

    def form_valid(self, form):
        login(self.request, form.get_user())
        LoginViewService(self.request).execute()
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


class UserProfileView(TemplateView):
    template_name = 'accounts/profile.html'
