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

from compras.models import Proveedor 
from baseapp.views import  is_cajero
from .forms import FormCompra, FormCompraDetalles, FormPagoCompra
from .models import Compra, CompraDetalles, EstadoCompra, Producto, PagoCompra, FormaPago

# Create your views here.

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
    compraDetalles = CompraDetalles.objects.filter(compra=id_compra, state = 0).select_related('producto').only('compra', 'producto', 'paquetes', 'valor_paquete', 'descuento_pre_iva', 'descuento_pos_iva',  'observacion', 'producto__nombre') # ideal para relaciones de uno a uno
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

#    context['productos'] = json.dumps(pr) # convertir a json
#    context['productos'] = json.dumps(productosArray, cls=DjangoJSONEncoder) # convertir a json
    context['productos'] = productosArray


    return render(request, "compras/compraRegistrada.html", context= context)


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

def guardarCompra(request, id = None):
    print("Lleganto a Compra")
    
    context = {}
    context['form_compra'] = FormCompra
    context['compra_list'] = Compra.objects.all()
 
    if id != None:
        # get_object_or_404 para manejo error 404 de manera automtica
        compra = get_object_or_404(Compra, id = id)
        
        if request.method == "POST":
            print("dentro del post")
            formRecibido = FormCompra(request.POST, instance= compra)
            print (request.POST)
            print(formRecibido.is_valid())
            print(id)
            print(request.POST.get('proveedor'))
            
            if formRecibido.is_valid():
                print("dentro del validd. Id= ", id )
                formRecibido.save()

            else:
                compra = Compra(
            proveedor = Proveedor.objects.get(id= int(request.POST.get('proveedor'))),
            fecha_compra = formRecibido.cleaned_data.get('fecha_compra'),
            valor_compra = 0,
            num_factura_proveedor = formRecibido.cleaned_data.get('num_factura_proveedor'),
            forma_pago = FormaPago.objects.get(pk = request.POST.get('forma_pago')),
            fecha_vence = dateformat.format(timezone.now(),'Y-m-d'),
            nota = formRecibido.cleaned_data.get('nota'),
            fecha_recibido = formRecibido.cleaned_data.get('fecha_recibido'),
            estado = EstadoCompra.objects.get(id = int(1)),
            updater = request.user.username
            )
            print(compra)
            print("user___________" + str(compra.updater))
            try:
                compra.save()
                id = compra.id
            except Exception as e:
                print("Error saving compra:", e)

            return redirect ('compras:comprasRegistradas', id_compra = id)
        else:
            print("no validado")
            return "Fuera del valid"
                
    else:
        print ("motodo no post")
        if id == None:
            print("no post no id")
            context['form_compra'] = FormCompra()
            context['title'] = "Crear nueva compra"
        else:
            print("no post con id")
            compra = Compra.objects.get(pk= id)
            print("217 ------  "  & compra)
            context['form_compra'] = FormCompra(instance=compra)
            context['title'] = "Editar compra Nº " + str(id)
            context['compra_id'] = compra.id  
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


def ajaxRegistrarCompraDetalle(request):
    # PARA GUARDAR DETALLES DE LA COMPRA 

    print("llegando a la vista ajaxRegistrarCompraDetalle")
    print(request.POST)
    fdetalles= FormCompraDetalles(request.POST or None)
    print ("form valido", fdetalles.is_valid())
    if fdetalles.is_valid():

        detalleCompra= CompraDetalles(fdetalles)
        '''
        compra = fdetalles.cleaned_data['compra']
        producto = fdetalles.cleaned_data.get('producto'),
        paquetes = fdetalles.cleaned_data.get('paquetes')
        unidades = fdetalles.cleaned_data.get('unidades')
        '''
        # crear un objeto detalle de compra con los datos enviados desde el form
        detalleCompra= CompraDetalles(
            compra = fdetalles.cleaned_data.get('compra'),
            producto = fdetalles.cleaned_data.get('producto'),
            paquetes = fdetalles.cleaned_data.get('paquetes'),
            unidades = fdetalles.cleaned_data.get('unidades'),
            valor_paquete = fdetalles.cleaned_data.get('valor_paquete'),
            descuento_pre_iva = fdetalles.cleaned_data.get('descuento_pre_iva'),
            descuento_pos_iva = fdetalles.cleaned_data.get('descuento_pos_iva'),
            iva = fdetalles.cleaned_data.get('iva'),
            flete = fdetalles.cleaned_data.get('flete'),
            neto = fdetalles.cleaned_data.get('neto'),
            observacion = fdetalles.cleaned_data.get('observacion')
            )

        print("antes de guardar")
        
        detalleCompra.save()
        
        print("despues de guardar")
        
        # recuperar el objeto creado

        detalleCreado = {
            'id': detalleCompra.pk,
            'compra' : detalleCompra.compra.id,
            'productoId' : detalleCompra.producto.id, 
            'codBar' : detalleCompra.producto.codigo_barras, 
            'productoNombre' : detalleCompra.producto.nombre,
            'paquetes' : detalleCompra.paquetes,
            'unidades' : detalleCompra.unidades,
            'valorPaquete' : detalleCompra.valor_paquete,
            'descuentoPreIva' : detalleCompra.descuento_pre_iva,
            'descuentoPosIva' : detalleCompra.descuento_pos_iva,
            'iva' : detalleCompra.iva,
            'flete' : detalleCompra.flete,
            'neto' : detalleCompra.neto,
            'observacion' : detalleCompra.observacion
            }
        print("detalleCompra" , detalleCompra)
        print("detalleCreado" , detalleCreado)
            
        response = {"success": True, "detalleCreado": detalleCreado}
        print (response)
        return JsonResponse(response)

    print("formulario invalido")
    ctx = {}
    ctx.update(csrf(request))
    fDetalle2 = render_crispy_form(fdetalles, context=ctx)
    response = {'success': False, 'detalle': fDetalle2}
    print (response)
    return JsonResponse(response)


# funcion para eliminar detalle de compra.
def eliminarDetalleCompra(request, pk):
    detalle = get_object_or_404(CompraDetalles, id=pk)
    id_compra = detalle.compra.id
    #detalle.delete() no se eliminará. será marcado como elimindo.
    detalle.state = 2
    detalle.deleted = timezone.now()
    detalle.deleter = request.user.id
    detalle.save()

    return redirect('compras:comprasRegistradas', id_compra = id_compra)


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
    template_name = "compras/objectsView.html"

    def get_context_data(self, **kwargs):
        context = super(ProveedorListView, self).get_context_data(**kwargs)
        context_object_name = "object_list"
        context['subtitulo'] = "Proveedores"
        return context




########################################################################################
########  VISTAS GENÉRICAS PARA DETALLES DE CADA MODELO ################################
########################################################################################


class ProveedorDetailView(generic.DetailView):
    model = Proveedor
    context_object_name = "object_detail"
    template_name = "compras/objectDetail.html"

