
from django.shortcuts import render
from django.views.generic.list import ListView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone, dateformat
from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect, HttpResponse
from django.template.context_processors import csrf
from crispy_forms.utils import render_crispy_form
from django.views import generic
from django.core.serializers import serialize
import json

from compras.models import Proveedor 
from baseapp.views import  is_cajero
from .forms import FormCompra, FormCompraDetalles, FormCompraDetallesFast, FormPagoCompra
from .models import Compra, CompraDetalles, EstadoCompra, Producto, PagoCompra, FormaPago



############################################################################################
## FUNCIONES PARA COMPRAS
############################################################################################

# ***************
@login_required() # requiere estar logueado
@user_passes_test(is_cajero ) # requiere ser cajero 
def compras(request):
        
    context = {}
    print("Lleganto a Compras")
    form = FormCompra(request.POST or None)
    context['form_compras'] = FormCompra    
    context['compra_list'] = Compra.objects.exclude(state=2) #excluyento los 2 que serían los eliminados

    if request.method =="POST":
        print("dentro del post")
        print("request.post", request.POST)
        form=context['form_compra'](data=request.POST) 
        print(form.is_valid())
        if form.is_valid() :
            print("dentro del valid")

            nuevaCompra= Compra(
                proveedor = form.cleaned_data.get('proveedor'),
                fecha_compra = form.cleaned_data.get('fecha_compra'),
                valor_compra = 0,
                num_factura_proveedor = form.cleaned_data.get('num_factura_proveedor'),
                forma_pago = form.cleaned_data.get('forma_pago'),
                fecha_vence = dateformat.format(timezone.now(),'Y-m-d'),
                nota = form.cleaned_data.get('nota'),
                fecha_recibido = form.cleaned_data.get('fecha_recibido'),
                estado = 0
            )
            nuevaCompra.save()
            print(nuevaCompra.id)
            return JsonResponse({'success': True,'menu': 'menuList'})
            return redirect('POS:comprasRegistradas', id_compra = nuevaCompra.id)
        else:
            for msg in form.errors:
                messages.error(request, form.errors[msg])
                print(msg)
            return render(request, "compras/compras.html", context)
    else:
        return render(request, "compras/compras.html", context)
# ********************

#############################################################################

@login_required() # requiere estar logueado
@user_passes_test(is_cajero ) # requiere ser cajero 
def comprasRegistradas(request, id_compra):
    '''Consulta los datos de la compra y los detalles de compra
    registrados para este id de compra.'''
    
    # get_object_or_404 para manejo error 404 de manera automtica
    compra = get_object_or_404(Compra, id = id_compra)
    
    print("compra registrada ss", compra)
    print("compra registrada sssss", compra.total)

    print(compra.proveedor)
#    ventaDetalles = VentaDetalles.objects.filter(venta=id_compra, state = 0).values_list('id', 'compra', 'producto', 'paquetes', 'valor_paquete', 'descuento', 'observacion', )
    compraDetalles = list(CompraDetalles.objects.filter(compra=id_compra, state = 0).select_related('producto').only('compra', 'producto', 'paquetes', 'valor_paquete', 'descuento_pre_iva', 'descuento_pos_iva',  'observacion', 'producto__nombre')) # ideal para relaciones de uno a uno
    compra2 = CompraDetalles.objects.filter(compra =id_compra).prefetch_related('producto').only('compra', 'producto', 'paquetes', 'valor_paquete', 'descuento_pre_iva', 'descuento_pos_iva',  'observacion', 'producto__nombre') # ideal para relaciones de uno a varios

    print(compraDetalles)
    # LISTAR PRODUCTOS
    productosArray =[]
    productos = Producto.objects.filter(estado = 1).prefetch_related('categoria').only('id', 'nombre', 'precio_venta', 'precio_mayor', 'cantidad_x_empaque', 'existencias', 'categoria_id__nombre', 'subcategoria__nombre')
    for prod in productos:
        pr={
            'id' : prod.id,
            'nombre': prod.nombre,
            'precioVenta' : prod.precio_venta,
            'costo' : prod.costo,
            'existencias' : prod.existencias,
            'categoria' : prod.categoria.nombre,
            'subcategoria' : prod.subcategoria.nombre,
            'cantidad_x_empaque': prod.cantidad_x_empaque,
        }
        productosArray.append(pr)
    print(productosArray)
    
    compra3 = CompraDetalles.objects.filter(compra =id_compra).select_related('producto').only('compra', 'producto', 'paquetes', 'valor_unitario', 'descuento_pre_iva', 'descuento_pos_iva',  'observacion', 'producto__nombre') # ideal para relaciones de uno a uno

    pago = PagoCompra(
        proveedor = compra.proveedor,
        compra = compra,
        fecha_pago = dateformat.format(timezone.now(),'Y-m-d'),
        forma_pago = FormaPago(id=1),
        updater = request.user.username,
        cajero = request.user
    )

    context = {}
    context['compra'] = compra
    context['form_compra'] = FormCompra(instance=compra)
    context['form_compra_detalles'] = FormCompraDetalles
    context['form_pago'] = FormPagoCompra(instance=pago)
#    context['ven3'] = ven3
    #context['ventaDetalles'] = dict_detalles
    context['compraDetalles'] = compraDetalles
    
    #Serializar los objetos CompraDetalles a formato JSON/
    json_compraDetalles = serialize('json', compraDetalles)

    # Convertir a un formato serializable
    context['detalles'] = json_compraDetalles


#    context['productos'] = json.dumps(pr) # convertir a json
#    context['productos'] = json.dumps(productosArray, cls=DjangoJSONEncoder) # convertir a json
    context['productos'] = productosArray


    return render(request, "compras/compraRegistrada.html", context= context)


@login_required() # requiere estar logueado
@user_passes_test(is_cajero ) # requiere ser cajero 
def comprasFast(request, id_compra):
    '''Consulta los datos de la compra y los detalles de compra
    registrados para este id de compra.'''
    
    # get_object_or_404 para manejo error 404 de manera automtica
    compra = get_object_or_404(Compra, id = id_compra)
        
    
    print("compra registrada ss", compra)
    print("compra registrada sssss", compra.total)

    print(compra.proveedor)
#    ventaDetalles = VentaDetalles.objects.filter(venta=id_compra, state = 0).values_list('id', 'compra', 'producto', 'paquetes', 'valor_paquete', 'descuento', 'observacion', )
    compraDetalles = CompraDetalles.objects.filter(compra=id_compra, state = 0).select_related('producto').only('compra', 'producto', 'paquetes', 'valor_paquete', 'observacion', 'producto__nombre') # ideal para relaciones de uno a uno
    compra2 = CompraDetalles.objects.filter(compra =id_compra).prefetch_related('producto').only('compra', 'producto', 'paquetes', 'valor_paquete', 'descuento_pre_iva', 'descuento_pos_iva',  'observacion', 'producto__nombre') # ideal para relaciones de uno a varios

    print(compraDetalles)
    # LISTAR PRODUCTOS
    productosArray =[]
    productos = Producto.objects.filter(estado = 1).prefetch_related('categoria').only('id', 'nombre', 'precio_venta', 'precio_mayor', 'cantidad_x_empaque', 'existencias', 'categoria_id__nombre', 'subcategoria__nombre')
    for prod in productos:
        pr={
            'id' : prod.id,
            'nombre': prod.nombre,
            'precioVenta' : prod.precio_venta,
            'costo' : prod.costo,
            'existencias' : prod.existencias,
            'categoria' : prod.categoria.nombre,
            'subcategoria' : prod.subcategoria.nombre,
            'cantidad_x_empaque': prod.cantidad_x_empaque,
        }
        productosArray.append(pr)
    print(productosArray)
    
    compra3 = CompraDetalles.objects.filter(compra =id_compra).select_related('producto').only('compra', 'producto', 'paquetes', 'valor_unitario', 'descuento_pre_iva', 'descuento_pos_iva',  'observacion', 'producto__nombre') # ideal para relaciones de uno a uno

    pago = PagoCompra(
        proveedor = compra.proveedor,
        compra = compra,
        fecha_pago = dateformat.format(timezone.now(),'Y-m-d'),
        forma_pago = FormaPago(id=1),
        updater = request.user.username,
        cajero = request.user
    )

    context = {}
    context['compra'] = compra
    context['form_compra'] = FormCompra(instance=compra)
    context['form_compra_detalles'] = FormCompraDetallesFast
    context['form_pago'] = FormPagoCompra(instance=pago)
#    context['ven3'] = ven3
    #context['ventaDetalles'] = dict_detalles
    context['compraDetalles'] = compraDetalles

#    context['productos'] = json.dumps(pr) # convertir a json
#    context['productos'] = json.dumps(productosArray, cls=DjangoJSONEncoder) # convertir a json
    context['productos'] = productosArray


    return render(request, "compras/compraFast.html", context= context)

########################################################################################
# funcion para crear compra. funcionando ?????
def crearCompra(request):
    context = {}
    print(request)
    form = FormCompra(request.POST or None)
    print("lleganto a crearCompra")

    if request.method =="POST":
        print("dentro del post")
        print("request.post", request.POST)
        print(form.is_valid())
        if form.is_valid() :
            print("dentro del valid")
            nuevaCompra= Compra(
                proveedor = form.cleaned_data.get('proveedor'),
                fecha_compra = form.cleaned_data.get('fecha_compra'),
                valor_compra = 0,
                num_factura_proveedor = form.cleaned_data.get('num_factura_proveedor'),
                forma_pago = form.cleaned_data.get('forma_pago'),
                fecha_vence = dateformat.format(timezone.now(),'Y-m-d'),
                nota = form.cleaned_data.get('nota'),
                fecha_recibido = form.cleaned_data.get('fecha_recibido'),
                estado = 0
            )
            nuevaCompra.save()
            print(nuevaCompra.id)
            return redirect('POS:comprasRegistradas', id_compra = nuevaCompra.id)
        else:
            for msg in form.errors:
                messages.error(request, form.errors[msg])
                print(msg)
            context['form_compra']=(request.POST) 
            return render(request, "compras/compras.html", context)

def guardarCompra(request, id=None):
    context = {}
    context['form_compra'] = FormCompra

    if request.method == "POST":
        formRecibido = FormCompra(request.POST, instance=Compra.objects.get(id=id) if id else None)

        if formRecibido.is_valid():
            compra = formRecibido.save(commit=False)
            compra.updater = request.user.username

            try:
                compra.save()
                id = compra.id
                return redirect('compras:comprasRegistradas', id_compra=id)
            except Exception as e:
                print("Error saving compra:", e)
                context['error_message'] = "Error al guardar la compra."
        else:
            context['error_message'] = "Por favor, corrija los errores del formulario."

    else:
        if id:
            compra = get_object_or_404(Compra, pk=id)
            context['form_compra'] = FormCompra(instance=compra)
            context['title'] = f"Editar compra Nº {id}"
            context['compra_id'] = id
        else:
            context['form_compra'] = FormCompra()
            context['title'] = "Crear nueva compra"

    return render(request, "compras/modalGuardarCompra.html", context)

# funcion para eliminar compra.
# En realidad no se elimina, se marca pero se conserva el registro.
def eliminarCompra(request, pk):
    compra = get_object_or_404(Compra, id=pk)
    id_compra = compra.id
    #compra.delete() no se eliminará. será marcado como elimindo.
    compra.state = 2
    compra.deleted = timezone.now()
    compra.deleter = request.user,id
    compra.save()

    return redirect('compras:compras')


def registrarpago(request, id_compra = None):
    print("llegando a la vista RegistarPago")
    print(request.POST)
    if request.method == 'POST':
        print ("dentro del post")
        formPagoCompra= FormPagoCompra (request.POST or None)
        print ("form valido", formPagoCompra.is_valid())
        if formPagoCompra.is_valid():
            # Crear una instancia de pago compra y asignar username
            pagocompra = PagoCompra(
                proveedor = formPagoCompra.cleaned_data.get('proveedor'),
                compra = formPagoCompra.cleaned_data.get('compra'),
                fecha_pago = formPagoCompra.cleaned_data.get('fecha_pago'),
                forma_pago = formPagoCompra.cleaned_data.get('forma_pago'),
                valor_pago = formPagoCompra.cleaned_data.get('valor_pago'),
                cajero = formPagoCompra.cleaned_data.get('cajero'),
                nota = formPagoCompra.cleaned_data.get('nota'),
                updater= request.user.username
            )
            pagocompra.save()# metodo save ha sido sobreescrito

            return redirect('compras:comprasRegistradas', id_compra = id_compra)
    
    # codigo para solicitudes GET
    compra = get_object_or_404(Compra, id=id_compra)
    pago = PagoCompra(

        proveedor = compra.proveedor,
        compra = compra,
        fecha_pago = dateformat.format(timezone.now(),'Y-m-d'),
        forma_pago = FormaPago(id=1),
        updater = request.user.username,
        cajero = request.user,
        valor_pago = 0,
        nota = "",


    )
    print("formateando fecha: ", dateformat.format(timezone.now(),'d-m-Y'))
    context = {}
    context['compra'] = compra
    context['form_pago'] = FormPagoCompra(instance=pago)
    return render(request, 'compras/pagoCompra.html', context)


def ajaxRegistrarCompraDetalle(request, id = None):
    # Verificar si la solicitud es POST
    if request.method == 'POST':
        # Crear el formulario con los datos de la solicitud
        fdetalles = FormCompraDetalles(request.POST, instance=CompraDetalles.objects.get(id=id)if id else None )
        
        # Verificar si el formulario es válido
        if fdetalles.is_valid():
            # Guardar el detalle de la compra
            detalleCompra = fdetalles.save(commit=False)
            
            detalleCompra.updater = request.user.username
            try:    
                detalleCompra.save()
                id = detalleCompra.id
                # Serializar el detalle creado para enviar como respuesta
                detalle_serializado = serialize('json', [detalleCompra,])
                print(detalle_serializado)

                # Devolver una respuesta JSON con el detalle creado
                return JsonResponse({"success": True, "detalleCreado": detalle_serializado})

            except Exception as e:
                print("Error saving Detalle de compra:", e)
                return JsonResponse({"success": False, "errors": e})

        else:
            # Si el formulario no es válido, devolver errores
            errors = fdetalles.errors.as_json()
            return JsonResponse({"success": False, "errors": errors})
    
    # Si la solicitud no es POST, devolver un error
    return JsonResponse({"success": False, "errors": "Esta vista solo acepta solicitudes POST."})





# funcion para eliminar detalle de compra.
def eliminarDetalleCompra(request):
    
    if request.method == 'POST': 
        print(request)
        # obtener el id a eliminar desde la solicitud post
        id = request.POST.get('id')
        try:
            print("solicita eliminar el id ", id )
            detalle = get_object_or_404(CompraDetalles, id=id)
            id_compra = detalle.compra.id
            #detalle.delete() no se eliminará. será marcado como elimindo.
            detalle.state = 2
            detalle.deleted = timezone.now()
            detalle.deleter = request.user.username
            detalle.save()  

            messages.success(request, "Eliminado Correctamente")
            return JsonResponse({'success': True})
            #return redirect('compras:comprasRegistradas', id_compra = id_compra)
        except:
            # Manejar el caso en el que el registro no existe
            return JsonResponse({'success': False})
    else:
        # Manejar el caso en el que la solicitud no sea AJAX o no sea POST
        return JsonResponse({'success': False})



def compras_por_producto(request, producto_id):
    # Obtener las últimas 5 compras para el producto especificado
    compras = Compra.objects.filter(producto_id=producto_id).order_by('-fecha_compra')[:5]
    
    context = {
        'compras': compras,
    }
    
    return render(request, 'compras_por_producto.html', context)


########################################################################################
########  VISTAS GENÉRICAS #############################################################
########################################################################################

##### PROVEEDOR ##################
class ProveedorListView(ListView):
    
    model = Proveedor
    paginate_by = 20  # if pagination is desired
    template_name = "baseapp/objectsView.html"

    queryset = Proveedor.objects.all().only('id', 'nombre', 'telefono')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subtitulo'] = "Proveedores"
        context['modelo'] = "proveedor"
        
        # Definimos los campos que deseamos mostrar en la tabla
        context['campos'] = ['id', 'nombre', 'telefono', 'Absolute_URL']

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

##### PROVEEDOR ##################
class EstadoCompraListView(ListView):
    
    model = EstadoCompra
    paginate_by = 20  # if pagination is desired
    template_name = "baseapp/objectsView.html"

    queryset = EstadoCompra.objects.all().only('id', 'nombre', 'descripcion')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subtitulo'] = "Estados de Compraes"
        context['modelo'] = "estadocompra"
        
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



########################################################################################
########  VISTAS GENÉRICAS PARA DETALLES DE CADA MODELO ################################
########################################################################################


class ProveedorDetailView(generic.DetailView):
    model = Proveedor
    context_object_name = "object_detail"
    template_name = "baseapp/objectDetail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        proveedor = self.get_object()
        object_detail = {}

        context['object_detail'] = {field.verbose_name: getattr(proveedor, field.name) for field in proveedor._meta.fields}
        return context


class EstadoCompraDetailView(generic.DetailView):
    model = EstadoCompra
    context_object_name = "object_detail"
    template_name = "baseapp/objectDetail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        estadoCompra = self.get_object()
        object_detail = {}

        context['object_detail'] = {field.verbose_name: getattr(estadoCompra, field.name) for field in estadoCompra._meta.fields}
        return context

