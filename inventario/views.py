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

    def get_context_data(self, **kwargs):
        context = super(CategoriaListView, self).get_context_data(**kwargs)
        context_object_name = "object_list"
        context['subtitulo'] = "Categorias"
        return context

##### SUB CATEGORIA ##################
class SubCategoriaListView(ListView):
    
    model = SubCategoria
    paginate_by = 20  # if pagination is desired
    template_name = "baseapp/objectsView.html"

    def get_context_data(self, **kwargs):
        context = super(SubCategoriaListView, self).get_context_data(**kwargs)
        context_object_name = "object_list"
        context['subtitulo'] = "SubCategorias"
        return context

##### ESTADO PRODUCTO ##################
class EstadoProductoListView(ListView):
    
    model = EstadoProducto
    paginate_by = 20  # if pagination is desired
    template_name = "baseapp/objectsView.html"

    def get_context_data(self, **kwargs):
        context = super(EstadoProductoListView, self).get_context_data(**kwargs)
        context_object_name = "object_list"
        context['subtitulo'] = "Estados del producto"
        return context


##### PRODUCTOS  ##################
class ProductoListView(ListView):
    
    model = Producto
    paginate_by = 10  # if pagination is desired
    template_name = "baseapp/objectsView.html"

    def get_context_data(self, **kwargs):
        context = super(ProductoListView, self).get_context_data(**kwargs)
        context_object_name = "object_list"
        context['subtitulo'] = "Productos"
        context['campos'] = {
            "field1": "nombre",
            "field2": "categoria",
            "field3": "costo",
            "field4": "precioVenta",
            "field5": "existencias",
            "field6": "imagen",
        }

        return context
    

########################################################################################
########  VISTAS GENÉRICAS PARA DETALLES DE CADA MODELO ################################
########################################################################################

class CategoriaDetailView(generic.DetailView):
    model = Categoria
    context_object_name = "object_detail"
    template_name = "baseapp/objectDetail.html"

class SubCategoriaDetailView(generic.DetailView):
    model = SubCategoria
    context_object_name = "object_detail"
    template_name = "baseapp/objectDetail.html"

class ProductoDetailView(generic.DetailView):
    model = Producto
    context_object_name = "object_detail"
    template_name = "baseapp/objectDetail.html"

class EstadoProductoDetailView(generic.DetailView):
    model = EstadoProducto
    context_object_name = "object_detail"
    template_name = "baseapp/objectDetail.html"
