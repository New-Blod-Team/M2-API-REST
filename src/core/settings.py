"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 3.0.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import pytz
from datetime import datetime, timedelta
from yaml import load, Loader

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Cargando la configuracion del proyecto
CONFIG = load(open(BASE_DIR + '/config.yml').read(), Loader=Loader)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = CONFIG['server']['secret']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = int(os.environ['DEBUG'])

ALLOWED_HOSTS = ['localhost', CONFIG['server']['domain'], 'www.' + CONFIG['server']['domain']]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # third party Apps
    'corsheaders',
    'rest_framework',
    # Local APPS
    'applications.authentication',
    'applications.api',
    'applications.player',
    # Payd modules.
    'applications.payment',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Django Cors
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'account': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'account',
        'USER': CONFIG['database']['user'],
        'PASSWORD': CONFIG['database']['password'],
        'HOST': CONFIG['database']['host'],
        'PORT': CONFIG['database']['port'],
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES';",
        },
    },
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'django_metin2',
        'USER': CONFIG['database']['user'],
        'PASSWORD': CONFIG['database']['password'],
        'HOST': CONFIG['database']['host'],
        'PORT': CONFIG['database']['port'],
        'OPTIONS': {},
    },
    'player': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'player',
        'USER': CONFIG['database']['user'],
        'PASSWORD': CONFIG['database']['password'],
        'HOST': CONFIG['database']['host'],
        'PORT': CONFIG['database']['port'],
        'OPTIONS': {
            'init_command': "CREATE DATABASE IF NOT EXISTS django_metin2;",
        },
    },
}


DATABASE_ROUTERS = {
    'applications.authentication.router.AuthenticationRouter',
    'applications.player.router.PlayerRouter'
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = '/home/data/www/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static")
]

# Django Cors 
CORS_ORIGIN_WHITELIST = [
    "http://localhost:4200",
    "http://127.0.0.1:9000"
]

# Mt2Web.py Config

# Configurations ingame
# Buff duration
# BUFFSTUF = '2018-08-13T00:00:00'

SERVERNAME = CONFIG['server']['name']
SERVERURL = CONFIG['server']['url']

BUFFSTUF = datetime(2030, 8, 13, 0, 0, 0, 00000, tzinfo=pytz.UTC)

# Final Stuff
FINALSTUFF = datetime(2030, 1, 1, 0, 0, 0, 00000, tzinfo=pytz.UTC)

# Config for storage the correct date of the activation
if CONFIG['register']['send_activation_email']:
    ACTIVATE = datetime(2035, 1, 1, 0, 0, 0, 00000, tzinfo=pytz.UTC)
else:
    ACTIVATE = datetime(2009, 1, 1, 0, 0, 0, 00000, tzinfo=pytz.UTC)

# Auth User Model for APP
CUSTOM_AUTH_USER_MODEL = 'authentication.Account'

CUSTOM_AUTHENTICATION_BACKENDS = ['applications.authentication.backends.ModelBackend']

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'applications.api.authentication.JWTAuthentication',
    )
}

## Banned a available account
BANNED = 'BLOCK'
ACCEPT = 'OK'

# Config of JWT Token
ALGORITHM = 'HS256'
SIGNING_KEY = SECRET_KEY
VERIFYING_KEY = None
AUDIENCE = None
ISSUER = None
TOKEN_TYPE_CLAIM = 'token_type'
USER_ID_FIELD = 'id'
USER_ID_CLAIM = 'user_id'
ACCESS_TOKEN_LIFETIME = timedelta(minutes=15)
AUTH_HEADER_TYPES = ('Bearer',)
AUTH_TOKEN_CLASSES = ('applications.api.tokens.AccessToken',)

# PaymentWall Config
PAYMENTWALL_PUBLIC_KEY = CONFIG['paymentwall']['public_key']
PAYMENTWALL_PRIVATE_KEY = CONFIG['paymentwall']['private_key']

# Mail Configuration
EMAIL_USE_TLS = True
EMAIL_HOST = CONFIG['mail']['host']
EMAIL_PORT = CONFIG['mail']['port']
EMAIL_HOST_USER = CONFIG['mail']['user']
EMAIL_HOST_PASSWORD = CONFIG['mail']['password']
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend' if DEBUG else 'django.core.mail.backends.smtp.EmailBackend'
