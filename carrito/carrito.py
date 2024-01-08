class Carrito:
    def __init__(self, request):
        self.request= request        
        self.session = request.session
        carrito = self.session.get("carrito")
        if not carrito:
            carrito=self.session["carrito"]={}
        self.carrito= carrito
        
    def agregar(self, producto):
        if(str(producto.id) not in self.carrito.keys()):
            self.carrito[producto.id]={
                "producto_id":producto.id,
                "nombre":producto.nombre,
                "precio":str(producto.precioVenta1),
                "cantidad":1,
                "imagen":producto.imagen.url
            }
        else:
            for key, value in self.carrito.items():
                if key == str(producto.id):
                    value["cantidad"]=value["cantidad"]+1
                    value["precio"]= str(float(value["cantidad"])* producto.precioVenta1)
                    break
        self.guardarCarrito()
    
    def guardarCarrito(self):
        self.session["carrito"]= self.carrito
        self.session.modified=True

    def eliminar(self, producto):
        producto.id=str(producto.id)
        if producto.id in self.carrito:
            del self.carrito[producto.id]
            self.guardarCarrito()

    def restaAlProducto(self, producto):
        for key, value in self.carrito.items():
            if key == str(producto.id):
                value["cantidad"]=value["cantidad"]-1
                value["precio"]= str(float(value["cantidad"])* producto.precioVenta1)
                if value["cantidad"]<1:
                    self.eliminar(producto)
                break
        self.guardarCarrito()

    def limpiarCarrito(self):
        self.session["carrito"]={}
        self.session.modified=True

