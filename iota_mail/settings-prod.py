from iota_mail.settings import *

import os

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB_NAME', 'iota_mail_db'),
        'USER': os.getenv('POSTGRES_USER', 'root'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'changeme'),
        'HOST': os.getenv('POSTGRES_HOST', 'db'),
        'PORT': os.getenv('POSTGRES_PORT', '5432')
    }
}

ALLOWED_HOSTS = ['*']

STATIC_ROOT = os.getenv('STATIC_ROOT', '/static')

# Googles SMTP server
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'j.innerbichler@gmail.com'
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'noreploy@zendi.com'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
