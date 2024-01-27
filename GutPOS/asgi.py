"""
ASGI config for GutPOS project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

# estando todo el setting en un archivo
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GutPOS.settings')

#estando separada la configuracion del setting en varios archivos
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GutPOS.settings.local')

application = get_asgi_application()
