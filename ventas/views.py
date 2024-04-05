from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect, HttpResponse 
from django.views.generic.list import ListView
from django.views import generic
from django.template.context_processors import csrf
from crispy_forms.utils import render_crispy_form
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test

from .forms import FormPagoVenta, FormVenta, FormVentaDetalles, FormPagoVenta
from .models import *
from carrito.carrito import Carrito
from baseapp.views import is_cajero

##############################################################################################
####     FUNCIONES PARA VENTAS 
##############################################################################################
def guardarventa(request, id = None):
    context = {}
#    form = FormVenta(request.POST or None)
    print("Lleganto a Ventas")
    context['form_venta'] = FormVenta    
    context['venta_list'] = Venta.objects.all()

    if request.method == "POST":
        print("dentro del post")
        formRecibido = FormVenta(request.POST)
        if formRecibido.is_valid():
            if id != None:
                venta = Venta.objects.get(pk=id)
            else:
                venta = Venta()
            venta.cliente = formRecibido.cleaned_data.get('cliente')
            venta.fecha_venta = formRecibido.cleaned_data.get('fecha_venta')
            venta.valor_venta = formRecibido.cleaned_data.get('valor_venta')
            venta.forma_pago = formRecibido.cleaned_data.get('forma_pago')
            venta.vendedor = formRecibido.cleaned_data.get('vendedor')
            venta.nota = formRecibido.cleaned_data.get('nota')
            venta.fecha_vence = formRecibido.cleaned_data.get('fecha_vence')
            venta.preventa = formRecibido.cleaned_data.get('preventa')
            venta.updater = request.user.username

            print(venta)
            venta.save()
            id = venta.id

            return redirect ('ventas:ventasRegistradas', id_venta = id)
                
    else:
        if id == None:
            print("no post no id")
            context['form_venta'] = FormVenta()
            context['title'] = "Crear nueva venta"
        else:
            print("no post con id")
            venta = Venta.objects.get(pk= id)
            print(venta)
            context['form_venta'] = FormVenta(instance=venta)
            context['title'] = "Editar venta Nº " + str(id)
            context['venta_id'] = venta.id  
        return render(request, "ventas/ventaForm.html", context)



# ***************
@login_required() # requiere estar logueado
@user_passes_test(is_cajero ) # requiere ser cajero 
def ventas(request):
    context = {}
#    form = FormVenta(request.POST or None)
    print("Lleganto a Ventas")
    context['form_venta'] = FormVenta    
    context['venta_list'] = Venta.objects.all()

    if request.method =="POST":
        print("dentro del post")
        print("request.post", request.POST)
        form=context['form_venta'](data=request.POST) 
        print(form.is_valid())
        if form.is_valid() :
            print("dentro del valid")
            nuevaVenta= Venta(
                cliente = form.cleaned_data.get('cliente'),
                fecha_venta = form.cleaned_data.get('fecha_venta'),
                valor_venta = form.cleaned_data.get('valor_venta'),
                forma_pago = form.cleaned_data.get('forma_pago'),
                vendedor = form.cleaned_data.get('vendedor'),
                nota = form.cleaned_data.get('nota'),
                fecha_vence = form.cleaned_data.get('fecha_vence'),
                preventa = form.cleaned_data.get('preventa'),
            )
            nuevaVenta.save()
            print(nuevaVenta.id)
            return redirect('POS:ventasRegistradas', id_venta = nuevaVenta.id)
        else:
            for msg in form.errors:
                messages.error(request, form.errors[msg])
                print(msg)
            return render(request, "ventas/ventas.html", context)
    else:
        return render(request, "ventas/ventas.html", context)
# ********************

# funcion para crear venta. funcionando ok
def crearVenta(request):
    context = {}
    print(request)
    form = FormVenta(request.POST or None)
    print("lleganto a crearVenta")

    if request.method =="POST":
        print("dentro del post")
        print("request.post", request.POST)
        print(form.is_valid())
        if form.is_valid() :
            print("dentro del valid")
            nuevaVenta= Venta(
                cliente = form.cleaned_data.get('cliente'),
                fecha_venta = form.cleaned_data.get('fecha_venta'),
                valor_venta = form.cleaned_data.get('valor_venta'),
                forma_pago = form.cleaned_data.get('forma_pago'),
                vendedor = form.cleaned_data.get('vendedor'),
                nota = form.cleaned_data.get('nota'),
                fecha_vence = form.cleaned_data.get('fecha_vence'),
                preventa = form.cleaned_data.get('preventa'),
            )
            nuevaVenta.save()
            print(nuevaVenta.id)
            return redirect('POS:ventasRegistradas', id_venta = nuevaVenta.id)
        else:
            for msg in form.errors:
                messages.error(request, form.errors[msg])
                print(msg)
            context['form_venta']=(request.POST) 
            return render(request, "ventas/ventas.html", context)

# funcion para crear venta. funcionando ok
def editarVenta(request, id_venta):
    print(request)
    form = FormVenta(request.POST or None)
    print("lleganto a editarVenta")

#    return redirect('POS:ventasRegistradas', id_venta = id_venta)
   
    if request.method =="POST":
        print("dentro del post")
        print("request.post", request.POST)
        print(form.is_valid())
        if form.is_valid() :
            print("dentro del valid")
            nuevaVenta= Venta(
                cliente = form.cleaned_data.get('cliente'),
                fecha_venta = form.cleaned_data.get('fecha_venta'),
                valor_venta = form.cleaned_data.get('valor_venta'),
                forma_pago = form.cleaned_data.get('forma_pago'),
                vendedor = form.cleaned_data.get('vendedor'),
                nota = form.cleaned_data.get('nota'),
                fecha_vence = form.cleaned_data.get('fecha_vence'),
                preventa = form.cleaned_data.get('preventa'),
            )
            nuevaVenta.save()
            print(nuevaVenta.id)
            return redirect('POS:ventasRegistradas', id_venta = nuevaVenta.id)


def ventasRegistradas(request, id_venta):
    '''Consulta los datos de la venta y los detalles de venta
    registrados para este id de venta.'''
    # get_object_or_404 para manejo error 404 de manera automtica
    venta = get_object_or_404(Venta, id = id_venta)
        
   # print("22777777777777777777777", venta.total)
    #print(venta.cliente)
#    ventaDetalles = VentaDetalles.objects.filter(venta=id_venta, state = 0).values_list('id', 'venta', 'producto', 'cantidad', 'valor_unitario', 'descuento', 'observacion', )
    ventaDetalles = VentaDetalles.objects.filter(venta=id_venta, state = 0).select_related('producto').only('venta', 'producto', 'cantidad', 'valor_unitario', 'descuento', 'observacion', 'producto__nombre') # ideal para relaciones de uno a uno
    ven2 = VentaDetalles.objects.filter(venta =id_venta).prefetch_related('producto').only('venta', 'producto', 'cantidad', 'valor_unitario', 'descuento', 'observacion', 'producto__nombre') # ideal para relaciones de uno a varios

    # LISTAR PRODUCTOS
    productosArray =[]
    productos = Producto.objects.filter(estado = 1).prefetch_related('categoria').only('id', 'nombre', 'precioVenta', 'precioMayor', 'existencias', 'categoria_id__nombre', 'subcategoria__nombre')
    for prod in productos:
        pr={
            'id' : prod.id,
            'nombre': prod.nombre,
            'precioVenta' : prod.precioVenta,
            'precioMayor' : prod.precioMayor,
            'existencias' : prod.existencias,
            'categoria' : prod.categoria.nombre,
            'subcategoria' : prod.subcategoria.nombre,
        }
        productosArray.append(pr)
  #  print(productosArray)
    
    ven3 = VentaDetalles.objects.filter(venta =id_venta).select_related('producto').only('venta', 'producto', 'cantidad', 'valor_unitario', 'descuento', 'observacion', 'producto__nombre') # ideal para relaciones de uno a uno

    pago = PagoVenta(
        cliente = venta.cliente,
        venta = venta,
        fecha_pago = dateformat.format(timezone.now(),'Y-m-d'),
        forma_pago = FormaPago(id=1),
        updater = request.user.username,
        cajero = request.user
    )

    context = {}
    context['venta'] = venta
    context['form_venta'] = FormVenta
    context['form_venta_detalles'] = FormVentaDetalles
    context['form_pago'] = FormPagoVenta(instance=pago)
    context['ven3'] = ven3
    #context['ventaDetalles'] = dict_detalles
    context['ventaDetalles'] = ventaDetalles

#    context['productos'] = json.dumps(pr) # convertir a json
#    context['productos'] = json.dumps(productosArray, cls=DjangoJSONEncoder) # convertir a json
    context['productos'] = productosArray


    return render(request, "ventas/ventaRegistrada.html", context= context)

def ajaxRegistrarVentaDetalle(request):
    # PARA GUARDAR DETALLES DE LA VENTA 

    print("llegando a la vista ajaxRegistrarVentaDetalle")
    print(request.POST)
    fdetalles= FormVentaDetalles(request.POST or None)
    print ("form valido", fdetalles.is_valid())
    if fdetalles.is_valid():

        detalleVenta= VentaDetalles(fdetalles)
        producto = fdetalles.cleaned_data['producto']
        val_uni = fdetalles.cleaned_data.get('valor_unitario')
        desc = fdetalles.cleaned_data.get('descuento')
        detalleVenta= VentaDetalles(
            venta = fdetalles.cleaned_data.get('venta'),
            producto = fdetalles.cleaned_data.get('producto'),
            cantidad = fdetalles.cleaned_data.get('cantidad'),
            valor_unitario = val_uni,
            descuento = desc,
            iva = producto.iva,
            neto = (val_uni - (val_uni*desc/100) + (val_uni*producto.iva/100)),
            observacion = fdetalles.cleaned_data.get('observacion'),            
            tarifa_aplicada = 0,
            costo = (producto.costo),
        )
        print("antes de guardar")
        
        detalleVenta.save()
        
        print("despues de guardar") 
        
        # recuperar el objeto creado
        detalleCreado = {
            'id': detalleVenta.id,
            'producto': detalleVenta.producto.id,
            'nombre': detalleVenta.producto.nombre,
            'cantidad': round(detalleVenta.cantidad,2),
            'valor_unitario':detalleVenta.valor_unitario,
            'descuento':detalleVenta.descuento,
            'iva': detalleVenta.iva,
            'neto': detalleVenta.neto,
            'observacion': detalleVenta.observacion,
            'total_venta': detalleVenta.venta.total
            }
        print(detalleVenta)
            
        response = {'success': True, 'detalleCreado': detalleCreado}
        print (response)
        return JsonResponse(response)

    print("formulario invalido")
    ctx = {}
    ctx.update(csrf(request))
    fDetalle2 = render_crispy_form(fdetalles, context=ctx)
    response = {'success': False, 'detalle': fDetalle2}
    print (response)
    return JsonResponse(response)

# funcion para eliminar detalle de venta.
def eliminarDetalleVenta(request, pk):
    detalle = get_object_or_404(VentaDetalles, id=pk)
    id_venta = detalle.venta.id
    #detalle.delete() no se eliminará. será marcado como elimindo.
    detalle.state = 2
    detalle.deleted = timezone.now()
    detalle.deleter = request.user,id
    detalle.save()

    return redirect('POS:ventasRegistradas', id_venta = id_venta)


def registrarpago(request, id_venta = None):
    print("llegando a la vista RegistarPago")
    print(request.POST)
    if request.method == 'POST':
        print ("dentro del post")
        formulariopagoVenta= FormPagoVenta(request.POST or None)
        print ("form valido", formulariopagoVenta.is_valid())
        if formulariopagoVenta.is_valid():
            # Crear una instancia de pago venta y asignar username
            pagoventa = PagoVenta(
                cliente = formulariopagoVenta.cleaned_data.get('cliente'),
                venta = formulariopagoVenta.cleaned_data.get('venta'),
                fecha_pago = formulariopagoVenta.cleaned_data.get('fecha_pago'),
                forma_pago = formulariopagoVenta.cleaned_data.get('forma_pago'),
                valor_pago = formulariopagoVenta.cleaned_data.get('valor_pago'),
                cajero = formulariopagoVenta.cleaned_data.get('cajero'),
                nota = formulariopagoVenta.cleaned_data.get('nota'),
                updater= request.user.username
            )
            pagoventa.save()# metodo save ha sido sobreescrito
            return redirect('POS:ventasRegistradas', id_venta = id_venta)
        
        return "Error al registrar el pago"
    
    # codigo para solicitudes GET
    venta = get_object_or_404(Venta, id=id_venta)
    pago = PagoVenta(
        cliente = venta.cliente,
        venta = venta,
        fecha_pago = dateformat.format(timezone.now(),'Y-m-d'),
        forma_pago = FormaPago(id=1),
        updater = request.user.username,
        cajero = request.user
    )
    print("formateando fecha: ", dateformat.format(timezone.now(),'d-m-Y'))
    context = {}
    context['venta'] = venta
    context['form_pago'] = FormPagoVenta(instance=pago)
    return render(request, 'ventas/pagoVenta.html', context)


def ajaxValidarVenta(request):
    
    fVenta= FormVenta(request.POST or None)
    if fVenta.is_valid():
        return {'success': True}
    
    ctx = {}
    ctx.update(csrf(request))
    fVenta2 = render_crispy_form(fVenta, context=ctx)
    response = {'success': False, 'venta' : fVenta2}
#    response = {'success': False}
    return JsonResponse(response)


########################################################################################
########## VISTAS GENERICAS PARA LISTAR LOS DIFERENTES MODELOS #########################
########################################################################################

##### ESTADO VENTA ##################
class EstadoVentaListView(ListView):
    
    model = EstadoVenta
    paginate_by = 20  # if pagination is desired
    template_name = "baseapp/objectsView.html"

    def get_context_data(self, **kwargs):
        context = super(EstadoVentaListView, self).get_context_data(**kwargs)
        context_object_name = "object_list"
        context['subtitulo'] = "Estados de Venta"
        return context




########################################################################################
########  VISTAS GENÉRICAS PARA DETALLES DE CADA MODELO ################################
########################################################################################

class EstadoVentaDetailView(generic.DetailView):
    model = EstadoVenta
    context_object_name = "object_detail"
    template_name = "baseapp/objectDetail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        estadoVenta = self.get_object()
        context['object_detail'] = {field.verbose_name: getattr(estadoVenta, field.name) for field in estadoVenta._meta.fields}
        return context
