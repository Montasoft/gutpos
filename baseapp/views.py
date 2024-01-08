from datetime import datetime
from django.utils import timezone, dateformat
import json
# import generic Views
from django.views import generic
from django.conf import settings
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
#from django.views.generic.edit import DeleteView

from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect, HttpResponse 
from django.contrib import messages
from django.template.context_processors import csrf
from crispy_forms.utils import render_crispy_form
from django.core.serializers import serialize
from import_export import resources
from django.contrib.auth.decorators import login_required, user_passes_test
#from .forms import FormPagoVenta, FormVenta, FormVentaDetalles, FormPagoVenta
from .models import *
from inventario.models import Producto
from ventas.models import Cliente
from carrito.carrito import Carrito
from .precargar import cargaInicial


def is_cajero(user):
    return user.is_superuser or user.groups.filter(name='Cajero').exists()

def index(request):
    carrito=Carrito(request)
    return render(request, "baseapp/index.html")
    #    return HttpResponse("Home")

def precargar(request):
    # vista creada para crecargar datos iniciales a la base de datos
    print("Se ha inicializador de manera correcta", cargaInicial())
    return render(request, "baseapp/index.html")

def POS(request):
    
    print("llegnado a POS")
    #menu = Menu.objects.all() #.prefetch_related('submenu')
    menu = Menu.objects.all()
    meList =[]
    for me in menu:
        print("Menuuuu; ", me.nombre )
        submenu = SubMenu.objects.filter(menu = me.id)   
        smList = []
        for sub in submenu:
            print("submenu; ", sub.nombre )
            smList.append({'id': sub.id,'nombre': sub.nombre,'orden': sub.orden,'icono': sub.icono,'enlace': sub.enlace, 'favorito': sub.favorito})
        meList.append({'orden': me.orden, 'nombre': me.nombre, 'submenu': smList})

    print ("items:", meList)

    return render(request, "baseapp/basePOS.html", {'menu': meList})



@login_required(login_url=settings.LOGIN_URL)
def producto(request, pk):

    producto = Producto.objects.get(id=pk)
    return render(request, "inventario/producto.html", {'producto':producto})


def servicios(request):
    return render(request, "baseapp/servicios.html")

#class VentasListView(ListView):
    
 #   cliente1 = Cliente(nombre="Clientes Varios", direccion= "sin definir", tipo_cliente= "esporádico", tipo_comercio = "ninguno")
  #  cliente1.save()

   # model = Venta
#    paginate_by = 100  # if pagination is desired
 #   template_name = "ventas/ventas.html"

  #  def get_context_data(self, **kwargs):
   #     context = super(VentasListView, self).get_context_data(**kwargs)
    #    context['subtitulo'] = "Subtitulo"
     #   context['form_venta'] = FormVenta
      #  return context

def AjaxGetOptionSelect(request):

    clientes= Cliente.objects.all()
    productos = Producto.objects.all()

    cliente_choices = []
    productos_choices = []

    for product in productos:
        productos_choices.append({'id': product.id, 'text': product.nombre})

    for cliente in clientes:
        cliente_choices.append({'id': cliente.id, 'text': cliente.nombre})

    datos_select = {"produc_json": productos_choices, "client_json" : cliente_choices }
    response = {"Generado": [datos_select]}
    #print(response)

    return JsonResponse(response)

########################################################################################
def pedirMenu(modelo = None, id= None):
    
    menu = Menu.objects.all() #recupero la lista de la tabla menu
    menuList =[]
    for me in menu:
        print("Menuuuu; ", me.nombre )
        submenu = SubMenu.objects.filter(menu = me.id)    #recupero de la tabla submenu
        smList = []
        for sub in submenu:
            print("submenu; ", sub.nombre )
            # crear la lista de submenu por cada menu
            smList.append({'id': sub.id,'nombre': sub.nombre,'orden': sub.orden,'icono': sub.icono,'enlace': sub.enlace, 'favorito': sub.favorito})
        menuList.append({'orden': me.orden, 'nombre': me.nombre, 'icono': me.icono, 'submenu': smList})

    print ("menu:", menuList)
    return JsonResponse({'success': True,'menu': menuList})


##### BANCOS  ##################
class BancoListView(ListView):
    
    model = Banco
    paginate_by = 20  # if pagination is desired
    template_name = "baseapp/objectsView.html"
    queryset = Banco.objects.all().only('id', 'nombre').annotate(field1=F('nombre'))

    def get_context_data(self, **kwargs):
        context = super(BancoListView, self).get_context_data(**kwargs)
        context_object_name = "object_list"
        context['subtitulo'] = "Bancos"
        context['campos'] = ['id', 'nombre' ]
        return context


##### DEPARTAMENTO ##################
class DepartamentoListView(ListView):
    
    model = Departamento
    paginate_by = 20  # if pagination is desired
    template_name = "baseapp/objectsView.html"

    def get_context_data(self, **kwargs):
        context = super(DepartamentoListView, self).get_context_data(**kwargs)
        context_object_name = "object_list"
        context['subtitulo'] = "Departamentos"
        return context
    
##### CIUDAD ##################
class CiudadListView(ListView):
    
    model = Ciudad
    paginate_by = 20  # if pagination is desired
    template_name = "baseapp/objectsView.html"

    def get_context_data(self, **kwargs):
        context = super(CiudadListView, self).get_context_data(**kwargs)
        context_object_name = "object_list"
        context['subtitulo'] = "Ciudades"
        return context
    
##### TIPO DE DOCUMENTO  ##################
class TipoDocumentoListView(ListView):
    
    model = TipoDocumento
    paginate_by = 20  # if pagination is desired
    template_name = "baseapp/objectsView.html"

    def get_context_data(self, **kwargs):
        context = super(TipoDocumentoListView, self).get_context_data(**kwargs)
        context_object_name = "object_list"
        context['subtitulo'] = "Tipos de documento"
        return context


##### FORMAS DE PAGO ##################
class FormaPagoListView(ListView):
    
    model = FormaPago
    paginate_by = 20  # if pagination is desired
    template_name = "baseapp/objectsView.html"

    def get_context_data(self, **kwargs):
        context = super(FormaPagoListView, self).get_context_data(**kwargs)
        context_object_name = "object_list"
        context['subtitulo'] = "Formas de pago"
        return context




########################################################################################
########  VISTAS GENÉRICAS PARA DETALLES DE CADA MODELO ################################
########################################################################################
 
class BancoDetailView(generic.DetailView):
    model = Banco
    context_object_name = "object_detail"
    template_name = "baseapp/objectDetail.html"

class DepartamentoDetailView(generic.DetailView):
    model = Departamento
    context_object_name = "object_detail"
    template_name = "baseapp/objectDetail.html"

class CiudadDetailView(generic.DetailView):
    model = Ciudad
    context_object_name = "object_detail"
    template_name = "baseapp/objectDetail.html"

class TipoDocumentoDetailView(generic.DetailView):
    model = TipoDocumento
    context_object_name = "object_detail"
    template_name = "baseapp/objectDetail.html"

class FormaPagoDetailView(generic.DetailView):
    model = FormaPago
    context_object_name = "object_detail"
    template_name = "baseapp/objectDetail.html"


