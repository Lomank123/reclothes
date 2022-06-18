# Auth settings

# Custom user model
AUTH_USER_MODEL = 'accounts.CustomUser'

# Login
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/auth/login/'

# Logout
LOGOUT_URL = '/auth/logout/'
LOGOUT_REDIRECT_URL = '/auth/login/'
