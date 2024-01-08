from django.shortcuts import render, HttpResponse
from inventario.models import Producto

# Create your views here.
def productos(request):
    productos = Producto.objects.all()

    return render(request, "tienda/productos.html", {'productos':productos})
    #    return HttpResponse("Home")

def tienda(request):
    productos = Producto.objects.all()
     
    return render(request, "tienda/tienda.html", {"productos":productos})
