from debug_toolbar import APP_NAME
from django.urls import path

from . import views

#app_name ="contacto"

urlpatterns=[
    path('', views.contacto, name="contacto"),
]