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
from baseapp.models import Banco
from carrito.carrito import Carrito
from .precargar import cargaInicial
from django.db.models import F, CharField, Case, Value, When


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

    # Precargar Proveedor
    banco2 = Banco(nombre = "No Determinado3", 
                    updater = request.user.username,)
    banco2.save()

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

##########################################################################
########## VISTAS GENERICAS PARA LISTAR LOS DIFERENTES MODELOS ###########
##########################################################################

##### BANCOS  ##################        
class BancoListView(ListView):
    
    model = Banco
    paginate_by = 20  # if pagination is desired
    template_name = "baseapp/objectsView.html"

    queryset = Banco.objects.all().only('id', 'nombre')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subtitulo'] = "Bancos"
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

##### DEPARTAMENTO ##################
class DepartamentoListView(ListView):
    
    model = Departamento
    paginate_by = 20  # if pagination is desired
    template_name = "baseapp/objectsView.html"

    queryset = Departamento.objects.all().only('id', 'nombre', 'cod_dane')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subtitulo'] = "Departamentos"

        # Definimos los campos que deseamos mostrar en la tabla
        context['campos'] = ['id', 'nombre', 'cod_dane', 'Absolute_URL']

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
    

##### CIUDAD ##################
class CiudadListView(ListView):
    
    model = Ciudad
    paginate_by = 20  # if pagination is desired
    template_name = "baseapp/objectsView.html"

    queryset = Ciudad.objects.all().only('id', 'nombre')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subtitulo'] = "Listado de Ciudades "
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

##### TIPO DE DOCUMENTO  ##################
class TipoDocumentoListView(ListView):
    
    model = TipoDocumento
    paginate_by = 20  # if pagination is desired
    template_name = "baseapp/objectsView.html"

    queryset = TipoDocumento.objects.all().only('id', 'cod', 'nombre')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subtitulo'] = "Tipo de documento"
        # Definimos los campos que deseamos mostrar en la tabla
        context['campos'] = ['id', 'cod', 'nombre', 'Absolute_URL']

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


##### FORMAS DE PAGO ##################
class FormaPagoListView(ListView):
    
    model = FormaPago
    paginate_by = 20  # if pagination is desired
    template_name = "baseapp/objectsView.html"
    
    queryset = FormaPago.objects.all().only('id', 'nombre', 'descripcion')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subtitulo'] = "Formas de pago"
        # Definimos los campos que deseamos mostrar en la tabla
        context['campos'] = ['id', 'nombre', 'descripcion', 'Absolute_URL']

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


##### TIPO DE CUENTA BANCARIA  ##################
class TipoCuentaBancariaListView(ListView):
    
    model = TipoCuentaBancaria
    paginate_by = 20  # if pagination is desired
    template_name = "baseapp/objectsView.html"

    queryset = TipoCuentaBancaria.objects.all().only('id', 'nombre')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subtitulo'] = "Tipo de cuenta bancaria"
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



########################################################################################
########  VISTAS GENÉRICAS PARA DETALLES DE CADA MODELO ################################
########################################################################################
 
class BancoDetailView(generic.DetailView):
    model = Banco
    context_object_name = "object_detail"
    template_name = "baseapp/objectDetail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        banco = self.get_object()
        object_detail = {}

        context['object_detail'] = {field.verbose_name: getattr(banco, field.name) for field in banco._meta.fields}
        return context

class DepartamentoDetailView(generic.DetailView):
    model = Departamento
    context_object_name = "object_detail"
    template_name = "baseapp/objectDetail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        departamento = self.get_object()
        context['object_detail'] = {field.verbose_name: getattr(departamento, field.name) for field in departamento._meta.fields}
        return context

class CiudadDetailView(generic.DetailView):
    model = Ciudad
    context_object_name = "object_detail"
    template_name = "baseapp/objectDetail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ciudad = self.get_object()
        context['object_detail'] = {field.verbose_name: getattr(ciudad, field.name) for field in ciudad._meta.fields}
        return context

class TipoDocumentoDetailView(generic.DetailView):
    model = TipoDocumento
    context_object_name = "object_detail"
    template_name = "baseapp/objectDetail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tipoDocumento = self.get_object()
        context['object_detail'] = {field.verbose_name: getattr(tipoDocumento, field.name) for field in tipoDocumento._meta.fields}
        return context


class FormaPagoDetailView(generic.DetailView):
    model = FormaPago
    context_object_name = "object_detail"
    template_name = "baseapp/objectDetail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        formaPago = self.get_object()
        context['object_detail'] = {field.verbose_name: getattr(formaPago, field.name) for field in formaPago._meta.fields}
        return context


class tipoCuentaBancariaDetailView(generic.DetailView):
    model = TipoCuentaBancaria
    context_object_name = "object_detail"
    template_name = "baseapp/objectDetail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tipoCuentaBancaria = self.get_object()
        context['object_detail'] = {field.verbose_name: getattr(tipoCuentaBancaria, field.name) for field in tipoCuentaBancaria._meta.fields}
        return context



