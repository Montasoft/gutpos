from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone, dateformat
from django.utils.translation import gettext as _
from django.db.models import F, Sum, FloatField     # para calcular el total de una orden de pedido

from baseapp.models import BaseModel, Tercero, FormaPago
from inventario.models import Producto

#######################################################################################
class EstadoVenta(BaseModel):
    '''
    1 creada (antes de agregar detalles)
    2 abierta (con detalles agregados)
    3 entregada (sin pago o pago parcial)
    4 pagada
    5 anulada (debe tener valor = 0)

    '''
    nombre = models.CharField(max_length=25)
    descripcion = models.CharField(max_length=150, null=True, blank=True)

    def __str__(self):
        return self.nombre
    
    def get_absolute_url(self):
        return reverse('ventas:EstadoVentaDetail', kwargs={'pk' :self.id})
    


#######################################################################################
class Cliente(Tercero):

    birthday = models.CharField(max_length=10, null=True, blank=True)
    tipo_cliente = models.CharField(max_length=150, null=True, blank=True)
    tipo_comercio = models.CharField(max_length=50, null=True, blank=True)
    ruta = models.CharField(max_length=20, null=True, blank=True)
    orden_ruta = models.IntegerField(default=0)
    
    class Meta:
        ordering =['nombre']

    def __str__(self):
        return  self.nombre

    def get_absolute_url(self):
        return reverse('POS:Cliente', kwargs={'pk' :self.id})

    def save(self, *args, **kwargs):
        ''' Al guardar actualizar fecha y usuario del registro 
            se recibe el usuario en el campo de updater
            pero si es registro nuevo se guardará en creater '''
        
        if not self.id:
            self.created = timezone.now()
            self.creater = self.updater
            self.updater = None
        else:
            print( "save - update")
            self.updated = timezone.now()
            self.updater = self.updater

        return super(Cliente, self).save(*args, **kwargs)


#######################################################################################
class PreVenta(BaseModel):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha_preventa = models.DateTimeField()
    valor_preventa = models.FloatField()
    forma_pago =  models.ForeignKey(FormaPago, on_delete=models.CASCADE)
    vendedor = models.ForeignKey(User, on_delete=models.CASCADE)
    nota = models.CharField(max_length= 250, null=True, blank= True)
    

    class Meta:
        ordering =['id']
        verbose_name = "preventa"
        verbose_name_plural = "preventas"

    def __str__(self):
        return  str(self.id)

    def save(self, *args, **kwargs):
        ''' Al guardar actualizar fecha y usuario del registro 
            se recibe el usuario en el campo de updater
            pero si es registro nuevo se guardará en creater '''
        
        if not self.id:
            self.created = timezone.now()
            self.creater = self.updater
            self.updater = None
        else:
            print( "save - update")
            self.updated = timezone.now()
            self.updater = self.updater

        return super(PreVenta, self).save(*args, **kwargs)


#######################################################################################
class Venta(BaseModel):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha_venta = models.DateField()
    valor_venta = models.DecimalField(max_digits=10, decimal_places=2)
    forma_pago =  models.ForeignKey (FormaPago, on_delete=models.CASCADE, default =1 )
    vendedor = models.ForeignKey(User, on_delete=models.CASCADE)
    nota = models.CharField(max_length= 250, null=True, blank= True)
    fecha_vence = models.DateField()
    preventa = models.ForeignKey(PreVenta, on_delete=models.CASCADE, null=True, blank= True)
    estado = models.ForeignKey(EstadoVenta, on_delete=models.CASCADE, default=1)

    class Meta:
        ordering =['id']
        verbose_name = "venta"
        verbose_name_plural = "ventas"

    def __str__(self):
        return  str(self.id)

    @property
    def total(self): 
        return self.ventadetalles_set.aggregate(
           total=Sum(F('cantidad')*(F('neto')), output_field=FloatField())
       )['total']

    def save(self, *args, **kwargs):
        ''' Al guardar actualizar fecha y usuario del registro 
            se recibe el usuario en el campo de updater
            pero si es registro nuevo se guardará en creater '''
        print("self.id", self.id)
        print("self.updater", self.updater)
        if not self.id:
            self.created = timezone.now()
            self.creater = self.updater
            self.updater = None
            self.estado = EstadoVenta(id=1) # creada
        else:
            print( "save - update")
            self.updated = timezone.now()
            self.updater = self.updater        
            if self.total != None:
                if self.estado == 1:
                    self.estado = EstadoVenta(id=2) # abierta


        return super(Venta, self).save(*args, **kwargs)


#######################################################################################
class VentaDetalles(BaseModel):

    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    valor_unitario = models.FloatField()
    descuento = models.FloatField(default =0)
    iva = models.IntegerField(default=0)
    neto = models.FloatField()
    observacion = models.CharField(max_length=250, null=True, blank= True )
    tarifa_aplicada = models.IntegerField()# cambiar dependiento de ta tabla de tarifas
    costo = models.FloatField()
    
    @property
    def calcularNeto(self):
        self.neto = self.valor_unitario - (self.valor_unitario*self.descuento/100) + (self.valor_unitario*self.iva/100)
    

    def to_dict(self):
        data = {}
        opts = self._meta        
        for f in opts.concrete_fields + opts.many_to_many:
            if isinstance(f, models.ManyToManyField):
                if self.pk is None:
                    data[f.name] = []
                else:
                    data[f.name] = list(f.value_from_object(self).values_list('pk', flat=True))
            elif isinstance(f, models.DateTimeField):
                if f.value_from_object(self) is not None:
                    data[f.name] = f.value_from_object(self).isoformat()
                else:
                    data[f.name] = None
            else:
                data[f.name] = f.value_from_object(self)
        return data

    class Meta:
        ordering =['id']
        verbose_name = "ventaDetalle"
        verbose_name_plural = "ventaDetalles"
   
    def __str__(self):  
        return f'{self.cantidad} unidades de {self.producto.nombre}'

    def get_cost(self):
        return self.producto.costo

    def save(self, *args, **kwargs):
        ''' Al guardar actualizar fecha y usuario del registro 
            se recibe el usuario en el campo de updater
            pero si es registro nuevo se guardará en creater '''
        
        if not self.id:
            self.created = timezone.now()
            self.creater = self.updater
            self.updater = None
        else:
            print( "save - update")
            self.updated = timezone.now()
            self.updater = self.updater

        return super(VentaDetalles, self).save(*args, **kwargs)


#######################################################################################
class PagoVenta(BaseModel):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    fecha_pago = models.DateField()
    forma_pago =  models.ForeignKey(FormaPago, on_delete=models.CASCADE)
    valor_pago = models.FloatField()
    cajero = models.ForeignKey(User, on_delete=models.CASCADE)
    nota = models.CharField(max_length= 250, null=True, blank= True  )
    
    class Meta:
        ordering =['id']
        verbose_name = "pagoVenta"
        verbose_name_plural = "Pagosventa"

    def __str__(self):
        return  str(self.valor_pago)

    def save(self, *args, **kwargs):
        ''' Al guardar actualizar fecha y usuario del registro 
            se recibe el usuario en el campo de updater
            pero si es registro nuevo se guardará en creater '''
        
        if not self.id:
            self.created = timezone.now()
            self.creater = self.updater
            self.updater = None
        else:
            print( "save - update")
            self.updated = timezone.now()
            self.updater = self.updater

        return super(PagoVenta, self).save(*args, **kwargs)

