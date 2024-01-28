from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
 
from .views import viewRegistro, cerrarSesion, log_in, loginRecov, miLogoutView, passReset, PasswResetDoneView, PasswResetConfirmView

app_name ="auth"
urlpatterns=[
    path('cerrarSesion', cerrarSesion, name="cerrarSesion"),
    path('loginRecov', loginRecov, name="loginRecov"),
    path('registro', viewRegistro.as_view(), name="autenticacion"),
    path('log_in', log_in, name="log_in"),
    path('login', LoginView.as_view(template_name='./registration/login.html'),  name='login'),
    path('logout/', miLogoutView.as_view(), name='logout'),
    
    
]   