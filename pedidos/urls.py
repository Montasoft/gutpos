from django.urls import path

from . import views

urlpatterns=[
    path('', views.procesarPedido , name="procesarPedido"),
    path('mostarCorreo', views.mostarCorreo , name="mostarCorreo"),
    
]