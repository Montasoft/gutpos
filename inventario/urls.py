from xml.dom.minidom import Document
from django.urls import path

from inventario import views
from django.conf import settings
from django.conf.urls.static import static

app_name ="inventario"

urlpatterns = [
    
    # Rutas para visualizar lista de los modelos de apoyo
    path('categorias', views.CategoriaListView.as_view(), name='categorias'),
    path('subcategorias', views.SubCategoriaListView.as_view(), name='subcategorias'),
    path('estadosproducto', views.EstadoProductoListView.as_view(), name='estadosproducto'),
    path('productos', views.ProductoListView.as_view(), name='productos'),
    
    # Rutas para visualizar detalles de cada modelos de apoyo
    path('categoria/<int:pk>', views.CategoriaDetailView.as_view(), name='categoriadetail'),
    path('subcategoria/<int:pk>', views.SubCategoriaDetailView.as_view(), name='subcategoriadetail'),
    path('estadoproducto/<int:pk>', views.EstadoProductoDetailView.as_view(), name='estadoproductodetail'),
    path('producto/<int:pk>', views.ProductoDetailView.as_view(), name='productodetail'),
    
    # Rutas para adicionar objetos nuevos a los modelos.
    path('Categoria/add', views.CategoriaCreateView.as_view(), name='CategoriaCreateView'),
    path('SubCategoria/add', views.SubCategoriaCreateView.as_view(), name='SubCategoriaCreateView'),
    path('EstadoProducto/add', views.EstadoProductoCreateView.as_view(), name='EstadoProductoCreateView'),
    path('Producto/add', views.ProductoCreateView.as_view(), name='P j43roductoCreateView'),

    # Rutas AJAX  
]


urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
