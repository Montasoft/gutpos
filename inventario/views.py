from django.shortcuts import render
from django.views.generic.list import ListView
from django.views import generic

from .models import *


########################################################################################
########  VISTAS GENÉRICAS #############################################################
########################################################################################

##### CATEGORIA ##################
class CategoriaListView(ListView):
    
    model = Categoria
    paginate_by = 20  # if pagination is desired
    template_name = "baseapp/objectsView.html"

    queryset = Categoria.objects.all().only('id', 'nombre')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subtitulo'] = "Categorías de productos"
        context['modelo'] = "categoria"
        context['url_crea'] = "inventario:CategoriaCreateView"

        # Definimos los campos que deseamos mostrar en la tabla
        context['campos'] = ['id', 'nombre', 'Absolute_URL']

        # Obtenemos la página actual
        page = self.request.GET.get('page')
        
        # Obtenemos los datos de la página actual
        object_data = []
        for obj in context['object_list']:
            obj_data = {}
            for campo in context['campos']:
                if campo == 'Absolute_URL':
                    obj_data[campo] = obj.get_absolute_url()
                else:
                    obj_data[campo] = getattr(obj, campo)
            object_data.append(obj_data)

        # Pasamos los datos de la página actual a la plantilla
        context['object_data'] = object_data
        return context


##### SUB CATEGORIA ##################
class SubCategoriaListView(ListView):
    
    model = SubCategoria
    paginate_by = 20  # if pagination is desired
    template_name = "baseapp/objectsView.html"
    
    queryset = SubCategoria.objects.all().only('id', 'nombre')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subtitulo'] = "Sub-categorías de productos"
        context['modelo'] = "SubCategoria"
        context['url_crea'] = "inventario:SubCategoriaCreateView"

        # Definimos los campos que deseamos mostrar en la tabla
        context['campos'] = ['id', 'nombre', 'Absolute_URL']

        # Obtenemos la página actual
        page = self.request.GET.get('page')
        
        # Obtenemos los datos de la página actual
        object_data = []
        for obj in context['object_list']:
            obj_data = {}
            for campo in context['campos']:
                if campo == 'Absolute_URL':
                    obj_data[campo] = obj.get_absolute_url()
                else:
                    obj_data[campo] = getattr(obj, campo)
            object_data.append(obj_data)

        # Pasamos los datos de la página actual a la plantilla
        context['object_data'] = object_data
        return context


##### ESTADO PRODUCTO ##################
class EstadoProductoListView(ListView):
    
    model = EstadoProducto
    paginate_by = 20  # if pagination is desired
    template_name = "baseapp/objectsView.html"

    queryset = EstadoProducto.objects.all().only('id', 'nombre')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subtitulo'] = "Estados del producto"
        context['modelo'] = "estadoproducto"
        context['url_crea'] = "inventario:EstadoProductoCreateView"

        # Definimos los campos que deseamos mostrar en la tabla
        context['campos'] = ['id', 'nombre', 'Absolute_URL']

        # Obtenemos la página actual
        page = self.request.GET.get('page')
        
        # Obtenemos los datos de la página actual
        object_data = []
        for obj in context['object_list']:
            obj_data = {}
            for campo in context['campos']:
                if campo == 'Absolute_URL':
                    obj_data[campo] = obj.get_absolute_url()
                else:
                    obj_data[campo] = getattr(obj, campo)
            object_data.append(obj_data)

        # Pasamos los datos de la página actual a la plantilla
        context['object_data'] = object_data
        return context


##### PRODUCTOS  ##################
class ProductoListView(ListView):
    
    model = Producto
    paginate_by = 10  # if pagination is desired
    template_name = "baseapp/objectsView.html"

    queryset = Producto.objects.all().only('id', 'nombre', 'costo', 'precio_venta', 'existencias' )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subtitulo'] = "Productos"
        context['modelo'] = "Producto"
        context['url_crea'] = "inventario:ProductoCreateView"

        # Definimos los campos que deseamos mostrar en la tabla
        context['campos'] = ['id', 'nombre', 'costo', 'precio_venta', 'existencias', 'Absolute_URL']

        # Obtenemos la página actual
        page = self.request.GET.get('page')
        
        # Obtenemos los datos de la página actual
        object_data = []
        for obj in context['object_list']:
            obj_data = {}
            for campo in context['campos']:
                if campo == 'Absolute_URL':
                    obj_data[campo] = obj.get_absolute_url()
                else:
                    obj_data[campo] = getattr(obj, campo)
            object_data.append(obj_data)

        # Pasamos los datos de la página actual a la plantilla
        context['object_data'] = object_data
        return context


########################################################################################
########  VISTAS GENÉRICAS PARA DETALLES DE CADA MODELO ################################
########################################################################################

class CategoriaDetailView(generic.DetailView):
    model = Categoria
    context_object_name = "object_detail"
    template_name = "baseapp/objectDetail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categoria = self.get_object()
        object_detail = {}

        context['object_detail'] = {field.verbose_name: getattr(categoria, field.name) for field in categoria._meta.fields}
        context['url_crea'] = "inventario:CategoriaCreateView"
        return context

class SubCategoriaDetailView(generic.DetailView):
    model = SubCategoria
    context_object_name = "object_detail"
    template_name = "baseapp/objectDetail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subCategoria = self.get_object()
        object_detail = {}

        context['object_detail'] = {field.verbose_name: getattr(subCategoria, field.name) for field in subCategoria._meta.fields}
        context['url_crea'] = "inventario:SubCategoriaCreateView"
        return context

class ProductoDetailView(generic.DetailView):
    model = Producto
    context_object_name = "object_detail"
    template_name = "baseapp/objectDetail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        producto = self.get_object()
        object_detail = {}

        # Convertir los campos del modelo en un diccionario con verbose_name como clave
        context['object_detail'] = {field.verbose_name: getattr(producto, field.name) for field in producto._meta.fields}
        
        # Añadir la URL de creación al contexto
        context['url_crea'] = "inventario:ProductoCreateView"
        return context

class EstadoProductoDetailView(generic.DetailView):
    model = EstadoProducto
    context_object_name = "object_detail"
    template_name = "baseapp/objectDetail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        estadoProducto = self.get_object()
        object_detail = {}

        context['object_detail'] = {field.verbose_name: getattr(estadoProducto, field.name) for field in estadoProducto._meta.fields}
        context['url_crea'] = "inventario:EstadoProductoCreateView"
        return context


########################################################################################
########  VISTAS GENÉRICAS PARA CREAR CADA MODELO ################################
########################################################################################
 
class CategoriaCreateView(generic.CreateView):
    model = Categoria
    fields = ['nombre']
    template_name = "baseapp/objectCreate.html" # Nombre de la plantilla donde se renderizará el formulario
    success_url = '/objectCreated'

    def form_valid(self, form):
        # Antes de guardar el formulario, establece el updater 
        if self.request.user.is_authenticated:
            form.instance.updater = self.request.user.username

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['modelo'] = "Categoria"
        context['url_crea'] = "inventario:CategoriaCreateView"
        return context
    

class SubCategoriaCreateView(generic.CreateView):
    model = SubCategoria
    fields = ['nombre']
    template_name = "baseapp/objectCreate.html" # Nombre de la plantilla donde se renderizará el formulario
    success_url = '/objectCreated'

    def form_valid(self, form):
        # Antes de guardar el formulario, establece el updater 
        if self.request.user.is_authenticated:
            form.instance.updater = self.request.user.username

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['modelo'] = "SubCategoria"
        context['url_crea'] = "inventario:SubCategoriaCreateView"
        return context

class ProductoCreateView(generic.CreateView):
    model = Producto
    fields = ['nombre', 'nombre', 'codigo_barras', 'categoria', 'subcategoria', 'costo', 'precio_venta', 'precio_mayor', 'iva', 'existencias', 'estado', 'dim_Alto', 'dim_Ancho', 'dim_fondo', 'peso', 'Nota', 'descripcion', 'cantidad_x_empaque', 'imagen']
    template_name = "baseapp/objectCreate.html" # Nombre de la plantilla donde se renderizará el formulario
    success_url = '/objectCreated'

    def form_valid(self, form):
        # Antes de guardar el formulario, establece el updater 
        if self.request.user.is_authenticated:
            form.instance.updater = self.request.user.username

        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['modelo'] = "Producto"
        context['url_crea'] = "inventario:ProductoCreateView"
        return context

class EstadoProductoCreateView(generic.CreateView):
    model = EstadoProducto
    fields = ['nombre']
    template_name = "baseapp/objectCreate.html" # Nombre de la plantilla donde se renderizará el formulario
    success_url = '/objectCreated'

    def form_valid(self, form):
        # Antes de guardar el formulario, establece el updater 
        if self.request.user.is_authenticated:
            form.instance.updater = self.request.user.username

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['modelo'] = "EstadoProducto"
        context['url_crea'] = "inventario:EstadoProductoCreateView"
        return context