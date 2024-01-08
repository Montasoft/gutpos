from django.urls import path

from .views import viewRegistro, cerrarSesion, log_in, loginRecov

app_name ="auth"
urlpatterns=[
    path('cerrarSesion', cerrarSesion, name="cerrarSesion"),
    path('loginRecov', loginRecov, name="loginRecov"),
    path('registro', viewRegistro.as_view(), name="autenticacion"),
    path('log_in', log_in, name="log_in"),

]