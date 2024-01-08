from django.shortcuts import redirect, render, HttpResponse
from django.contrib.auth.decorators import login_required
from carrito.carrito import Carrito
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail

from pedidos.models import Pedido, PedidoDetalle


@login_required(login_url='/autenticacion/logear/')
def procesarPedido(request):
    pedido= Pedido.objects.create(user=request.user)
    carrito = Carrito(request)
    detallePedido = list()
    for key, value in carrito.carrito.items():
        detallePedido.append(PedidoDetalle(
            producto_id = key,
            cantidad =value["cantidad"],
            user = request.user,
            pedido= pedido

        ))  
    PedidoDetalle.objects.bulk_create(detallePedido)

    nombreUsuario=request.user.username,
    emailUsuario=request.user.email,
    print("email:::::", emailUsuario, "nombreee_:::", nombreUsuario)

    enviar_mail(
        pedido=pedido,
        detallePedido=detallePedido,
        nombreUsuario=request.user.username,
        emailUsuario=request.user.email,
    )

    messages.success(request, "El pedido se ha creado correctamente")
    
    print("ENVIAR PEDIDO")
    return redirect("../tienda/tienda")

def enviar_mail(**kwargs):
    print("recibo los datos")
    print(kwargs.get("pedido.id"))
    print(kwargs.get("nombreUsuario"))
    print(kwargs.get("emailUsuario"))
    print( kwargs.get("detallePedido"))
    asunto = "gracias por su pedido"
    mensaje=render_to_string("emails/pedido.html", {
        "pedido": kwargs.get("pedido"),
        "detallePedido": kwargs.get("detallePedido"),
        "nombreUsuario": kwargs.get("nombreUsuario"),
        "emailUsuario": kwargs.get("emailUsuario")
    })

    mensajeTexto = strip_tags(mensaje)
    from_email ="soporte@solcatsas.com"
    to= kwargs.get("emailUsuario")

    send_mail(asunto, mensajeTexto,from_email,[to],html_message=mensaje)



def mostarCorreo(request):
    userActual = request.user.email
    nombre = request.user.username
    print("email:::::", userActual, "nombreee_:::", nombre)
    
    return (nombre)
