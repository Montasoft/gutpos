from xml.dom.minidom import Document
from django.urls import path

from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name ="baseapp"

urlpatterns = [

    path('servicios', views.servicios, name="servicios"),
    path('POS', views.POS, name="POS"),
    path('precargar', views.precargar, name="precargar"),

    # Rutas para visualizar lista de los modelos de apoyo
    path('bancos', views.BancoListView.as_view(), name='bancos'),
    path('departamentos', views.DepartamentoListView.as_view(), name='departamentos'),
    path('ciudades', views.CiudadListView.as_view(), name='ciudades'),
    path('tiposdocumento', views.TipoDocumentoListView.as_view(), name='tiposdocumento'),
    path('formaspago', views.FormaPagoListView.as_view(), name='formaspago'),
    path('tipocuentabancaria', views.TipoCuentaBancariaListView.as_view(), name='tipocuentabancaria'),

    # Rutas para visualizar detalles de cada modelos de apoyo
    path('banco/<int:pk>', views.BancoDetailView.as_view(), name='bancodetail'),
    path('departamento/<int:pk>', views.DepartamentoDetailView.as_view(), name='departamentodetail'),
    path('ciudad/<int:pk>', views.CiudadDetailView.as_view(), name='ciudaddetail'),
    path('tipodocumento/<int:pk>', views.TipoDocumentoDetailView.as_view(), name='tipodocumentodetail'),
    path('tipocuentabancaria/<int:pk>', views.tipoCuentaBancariaDetailView.as_view(), name='tipocuentabancariadetail'),
    path('formapago/<int:pk>', views.FormaPagoDetailView.as_view(), name='formapagodetail'),

    # Rutas para adicionar objetos nuevos a los modelos.
    path('Banco/add', views.BancoCreateView.as_view(), name='BancoCreateView'),
    path('Departamento/add', views.DepartamentoCreateView.as_view(), name='DepartamentoCreateView'),
    path('Ciudad/add', views.CiudadCreateView.as_view(), name='CiudadCreateView'),
    path('TipoDocumento/add', views.TipoDocumentoCreateView.as_view(), name='TipoDocumentoCreateView'),
    path('FormaPago/add', views.FormaPagoCreateView.as_view(), name='FormaPagoCreateView'),
    path('TipoCuentaBancaria/add', views.TipoCuentaBancariaCreateView.as_view(), name='TipoCuentaBancariaCreateView'),

    # ruta para mostrar después de una creación exitosa
    path('objectCreated', views.objectCreated, name='objectCreated'),


    # Rutas AJAX
    path('pedirMenu', views.pedirMenu, name="pedirMenu"),
    path('AjaxGetOptionSelect', views.AjaxGetOptionSelect, name="AjaxGetOptionSelect"),

    path('', views.index, name="index"),
]

urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
