"""
WSGI config for GutPOS project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

#estando todo en un solo archivo settings
#os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GutPOS.settings')

#estando separada la configuracion del setting en varios archivos
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GutPOS.settings.local')

application = get_wsgi_application()
