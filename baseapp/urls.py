from xml.dom.minidom import Document
from django.urls import path

from baseapp import views
from django.conf import settings
from django.conf.urls.static import static

app_name ="baseapp"

urlpatterns = [

    path('', views.index, name="index"),
    path('servicios', views.servicios, name="servicios"),
    path('POS', views.POS, name="POS"),
    path('precargar', views.precargar, name="precargar"),

    # Rutas para visualizar lista de los modelos de apoyo
    path('bancos', views.BancoListView.as_view(), name='bancos'),
    path('departamentos', views.DepartamentoListView.as_view(), name='departamentos'),
    path('ciudades', views.CiudadListView.as_view(), name='ciudades'),
    path('tiposdocumento', views.TipoDocumentoListView.as_view(), name='tiposdocumento'),
    path('formaspago', views.FormaPagoListView.as_view(), name='formaspago'),


    # Rutas para visualizar detalles de cada modelos de apoyo
    path('banco/<int:pk>', views.BancoDetailView.as_view(), name='bancodetail'),
    path('departamento/<int:pk>', views.DepartamentoDetailView.as_view(), name='departamentodetail'),
    path('ciudad/<int:pk>', views.CiudadDetailView.as_view(), name='ciudaddetail'),
    path('tipodocumento/<int:pk>', views.TipoDocumentoDetailView.as_view(), name='tipodocumentodetail'),
    path('formapago/<int:pk>', views.FormaPagoDetailView.as_view(), name='formapagodetail'),

    # Rutas AJAX
    path('pedirMenu', views.pedirMenu, name="pedirMenu"),
    path('AjaxGetOptionSelect', views.AjaxGetOptionSelect, name="AjaxGetOptionSelect"),

    
]

urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
