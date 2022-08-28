import os


# Auth settings

# Custom user model
AUTH_USER_MODEL = 'accounts.CustomUser'

# Login
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/auth/login/'

# Logout
LOGOUT_URL = '/auth/logout/'
LOGOUT_REDIRECT_URL = '/auth/login/'

# Dev superuser credentials
# python manage.py createsuperuser --noinput
DJANGO_SUPERUSER_USERNAME = os.environ.get('DJANGO_SUPERUSER_USERNAME')
DJANGO_SUPERUSER_EMAIL = os.environ.get('DJANGO_SUPERUSER_EMAIL')
DJANGO_SUPERUSER_PASSWORD = os.environ.get('DJANGO_SUPERUSER_PASSWORD')
