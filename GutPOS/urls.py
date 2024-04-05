"""GutPOS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

#from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView
#from django.contrib.auth.views import PasswordChangeDoneView,  passwpassord_reset, password_reset_done, password_reset_confirm, password_reset_complete

urlpatterns = [
    path('admin/', admin.site.urls),
#    path('blog/', include('BlogApp.urls')),
    path('contacto/', include('contacto.urls')),
    path('auth/', include('autenticacion.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('tienda/', include('tienda.urls')),
    path('carrito/', include('carrito.urls')),
    path('pedidos/', include('pedidos.urls')),
    path('compras/', include('compras.urls')),
    path('ventas/', include('ventas.urls')),
    path('inventario/', include('inventario.urls')),
    path('', include('baseapp.urls')),
 #   path(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
  #  path(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
   # path(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    #    auth_views.password_reset_confirm, name='password_reset_confirm'),
 #   path(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
    
    path('password_reset', auth_views.PasswordResetView.as_view(template_name=   './registration/password_reset.html'), name='password_reset'),
    path('password_reset/done', auth_views.PasswordResetDoneView.as_view(template_name='./registration/password_reset_done.html'),  name='password_reset_done'),  
    path('password_change', auth_views.PasswordChangeView.as_view(template_name='./registration/login.html'),  name='password_change'),
    path('password_change/done', auth_views.PasswordChangeDoneView.as_view(template_name='./registration/password_reset_done.html'),  name='password_change_done'),
  #  path('password_reset', passReset.as_view(),  name='password_reset'),   
  #  path('password_reset/done', PasswResetDoneView.as_view(), name='password_reset_done'), 
 #   path('password_reset/done', PasswResetDoneView.as_view(template_name='registration/password_reset_done.html'),  name='password_reset_done'),  
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='./registration/password_reset_confirm.html'),  name='password_reset_confirm'),
   # path('reset/done', PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),  name='password_reset_complete')

]

