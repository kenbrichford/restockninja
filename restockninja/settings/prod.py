from .base import *
import django_heroku
import dj_database_url


ALLOWED_HOSTS = ['.restock.ninja', 'restockninja.herokuapp.com']


# Security settings
SECURE_SSL_REDIRECT = True

SECURE_CONTENT_TYPE_NOSNIFF = True

SECURE_BROWSER_XSS_FILTER = True

SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SECURE = True

X_FRAME_OPTIONS = 'DENY'

SECURE_HSTS_SECONDS = 31536000

SECURE_HSTS_INCLUDE_SUBDOMAINS = True

SECURE_HSTS_PRELOAD = True


# Error logging
ADMINS = [('Kenning Brichford', 'kenning@brichford.com')]


# Database
db_from_env = dj_database_url.config()

DATABASES = {'default': db_from_env}


# Activate Django-Heroku
django_heroku.settings(locals())
