from django.urls import path

from . import views

app_name ="carrito"

urlpatterns = [
    path('agregar/<int:producto_id>/', views.agregarProducto, name="agregar"),
    path('eliminar/<int:producto_id>/', views.eliminarProducto, name="eliminar"),
    path('resta/<int:producto_id>/', views.restarProducto, name="restar"),
    path('limpiar/', views.limpiarProducto, name="Limpiar"),
    
]
