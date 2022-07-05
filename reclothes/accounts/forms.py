from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


user_model = get_user_model()


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = user_model
        fields = ("username", )
