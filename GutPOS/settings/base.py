"""
Django settings for GUTPOS project.
"""

import environ
import os
from pathlib import Path
from dotenv import load_dotenv
from django.contrib.messages import constants as mensajes

load_dotenv() # carga las variables desde el archivo .env

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# environ init
#environ.Env.read_env(os.path.join(BASE_DIR, '.env'))
env = environ.Env()
environ.Env.read_env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG', default=False)

ALLOWED_HOSTS = tuple(env.list('ALLOWED_HOSTS', default=[]))


# Application definition

BASE_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'import_export'
    
]

LOCAL_APPS = [
#    'tienda',
    'compras',
    'baseapp',
    'ventas',
    'inventario',
 #   'BlogApp',
    'contacto',
    'carrito',
    'pedidos',
    'autenticacion',
]

THIRD_APPS=[
    'crispy_forms',
    'fontawesomefree',
    'MySQLdb',
]

INSTALLED_APPS = BASE_APPS + LOCAL_APPS + THIRD_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'GutPOS.urls'

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
                'carrito.context_processor.importeTotalCarro',
            ],
            'libraries':{
            'custom_tags': 'baseapp.custom_tags',
            }
        },
    },
]

WSGI_APPLICATION = 'GutPOS.wsgi.application'



# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'es-us'

#TIME_ZONE = 'UTC'

DATE_INPUT_FORMATS = ('%d-%m-%Y','%Y-%m-%d')

TIME_ZONE = 'America/Bogota'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/


STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'
MEDIA_URL =  '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR,'media')

LOGIN_URL = '/auth/log_in'
LOGIN_REDIRECT_URL = 'baseapp:index'



# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CRISPY_TEMPLATE_PACK= 'bootstrap4'

MESSAGE_TAGS = {
    mensajes.DEBUG: 'debug',
    mensajes.INFO: 'info',
    mensajes.SUCCESS: 'success',
    mensajes.WARNING: 'warning',
    mensajes.ERROR: 'danger',
}


# Configuración regional para formato de moneda
USE_L10N = True
USE_THOUSAND_SEPARATOR = True

