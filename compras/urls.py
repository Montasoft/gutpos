from django.urls import path

from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name ="compras"

urlpatterns = [

    path('crearcompra', views.crearCompra, name="crearcompra"),
    path('guardarCompra', views.guardarCompra , name="guardarCompra"),
    path('guardarCompra/<int:id>/', views.guardarCompra , name="guardarCompra"),
    path('eliminarCompra/<int:pk>/', views.eliminarCompra , name="eliminarCompra"),
    
  
   # path('editarcompra/<int:id_compra>/', views.editarcompra, name="editarcompra"),
    path('comprasRegistradas/<int:id_compra>', views.comprasRegistradas, name="comprasRegistradas"),
    path('comprasFast/<int:id_compra>', views.comprasFast, name="comprasFast"),
    path('eliminarDetalleCompra/', views.eliminarDetalleCompra, name="eliminarDetalleCompra"),
    path('eliminarDetalleCompra/<int:pk>/', views.eliminarDetalleCompra, name="eliminarDetalleCompra"),
    
    path('registrarpago', views.registrarpago, name="registrarpago"),
    path('registrarpago/<int:id_compra>', views.registrarpago, name="registrarpago"),
 #   path('ajaxValidarcompra', views.ajaxValidarcompra, name="ajaxValidarcompra"),
    path('ajaxRegistrarCompraDetalle', views.ajaxRegistrarCompraDetalle, name="ajaxRegistrarCompraDetalle"),
    path('ajaxRegistrarCompraDetalle/<int:id>/', views.ajaxRegistrarCompraDetalle, name="ajaxRegistrarCompraDetalle"),

    
   # path('AjaxGetOptionSelect', views.AjaxGetOptionSelect, name="AjaxGetOptionSelect"),

    # Rutas para visualizar lista de los modelos de apoyo
    path('proveedores', views.ProveedorListView.as_view(), name='proveedor'),
    path('estadocompra', views.EstadoCompraListView.as_view(), name='estadoCompra'),

    # Rutas para visualizar detalles de cada modelos de apoyo
    path('proveedordetail/<int:pk>', views.ProveedorDetailView.as_view(), name='proveedordetail'),
    

    path('', views.compras , name="compras"),

]

urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
