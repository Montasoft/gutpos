from .base import *
from decouple import config

# para corregir error con mySQL
import pymysql
pymysql.install_as_MySQLdb()

# decouple permite trabajar las variables de entorno
# para recuperar:: EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')

# SECURITY WARNING: don't run with debug turned on in production!
#DEBUG = True

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=lambda v: [s.strip() for s in v.split(',')])

ALLOWED_HOSTS = ['*']
# con ['*'] para recibir conexión de todos los orígnes
# limitado es []
# y ejecutar el servidor con "python manage.py runserver 0.0.0.0:8000"
# permitirá conectarte desde el celular.
# desde el movil o el pc ejecutar con la ip fisica del server 192.168.1.58:8000


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

  
#Conectar al SQLite
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
"""
# CONECTAR A MySQL
DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'gutpos',
            'USER': config('DBUSER'),
            'PASSWORD': config('DBPASS'),
            'HOST': 'localhost',
            'PORT': '3360',
        }
    }
"""

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/static/'

# configuración de correo electrónico

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST="smtp.gmail.com"
EMAIL_PORT = 587 #465
EMAIL_HOST_USER = 'miniabastoslaroca@gmail.com'
EMAIL_HOST_USER = 'pruebasgutpos@gmail.com'
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
#EMAIL_USE_SSL = True
EMAIL_USE_TLS = True
#EMAIL_TIMEOUT =
#EMAIL_SSL_KEYFILE= 
#EMAIL_SSL_CERTFILE = 
print(EMAIL_HOST_PASSWORD)

