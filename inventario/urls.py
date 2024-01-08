from xml.dom.minidom import Document
from django.urls import path

from baseapp import views
from django.conf import settings
from django.conf.urls.static import static

app_name ="invantario"

urlpatterns = [

    path('productos', views.ProductoListView.as_view(), name='productos'),
    path('producto/<int:pk>', views.producto, name="producto"),
    
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
    
    # Rutas AJAX  
]

urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
