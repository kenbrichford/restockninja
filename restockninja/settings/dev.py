from .base import *


DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']


# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        
        'NAME': 'restockninja',
        
        'HOST': '127.0.0.1',
    }
}