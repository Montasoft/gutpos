from xml.dom.minidom import Document
from django.urls import path

from ventas import views
from django.conf import settings
from django.conf.urls.static import static

app_name ="ventas"

urlpatterns = [

    #path('ventas', views.VentasListView.as_view() , name="ventas"),
    path('guardarventa', views.guardarventa, name="guardarventa"),
    path('guardarventa/<int:id>/', views.guardarventa , name="guardarventa"),
    path('crearVenta', views.crearVenta, name="crearVenta"),
    path('editarVenta/<int:id_venta>/', views.editarVenta, name="editarVenta"),
    path('ventasRegistradas/<int:id_venta>', views.ventasRegistradas, name="ventasRegistradas"),
    path('eliminarDetalleVenta/<int:pk>/', views.eliminarDetalleVenta, name="eliminarDetalleVenta"),
    path('', views.ventas , name="ventas"),

#    path('registrarpago', views.registrarpago, name="registrarpago"),
    path('registrarpago/<int:id_venta>', views.registrarpago, name="registrarpago"),
    path('ajaxValidarVenta', views.ajaxValidarVenta, name="ajaxValidarVenta"),
    path('ajaxRegistrarVentaDetalle', views.ajaxRegistrarVentaDetalle, name="ajaxRegistrarVentaDetalle"),
    
    # Rutas para visualizar lista de los modelos de apoyo
    path('estadosventa', views.EstadoVentaListView.as_view(), name='estadosventa'),
    path('clientes', views.ClienteListView.as_view(), name='clientes'),

    # Rutas para visualizar detalles de cada modelos de apoyo
    path('estadoventa/<int:pk>', views.EstadoVentaDetailView.as_view(), name='EstadoVentaDetail'),
    path('cliente/<int:pk>', views.ClienteDetailView.as_view(), name='ClienteDetailView'),

    # Rutas para adicionar objetos nuevos a los modelos.
    path('estadoventa/add', views.EstadoVentaCreateView.as_view(), name='EstadoVentaCreateView'),
    path('cliente/add', views.ClienteCreateView.as_view(), name='ClienteCreateView'),



    # Rutas AJAX
    
]

urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
