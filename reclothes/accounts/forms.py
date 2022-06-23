from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


user_model = get_user_model()


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = user_model
        fields = ("username", )
