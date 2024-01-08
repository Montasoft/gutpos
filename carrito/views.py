from django.shortcuts import render, redirect
from .carrito import Carrito
from inventario.models import Producto

def agregarProducto(request, producto_id):
    carrito = Carrito(request)
    producto = Producto.objects.get(id=producto_id)
    carrito.agregar(producto=producto)

    return redirect("tienda")


def eliminarProducto(request, producto_id):
    carrito = Carrito(request)
    producto = Producto.objects.get(id=producto_id)
    carrito.eliminar(producto=producto)

    return redirect("tienda")

def restarProducto(request, producto_id):
    carrito = Carrito(request)
    producto = Producto.objects.get(id=producto_id)
    carrito.restaAlProducto(producto=producto)

    return redirect("tienda")

def limpiarProducto(request):
    carrito = Carrito(request)
    carrito.LimpiarCarrito()
    
    return redirect("tienda")
