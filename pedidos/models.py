from django.db import models
from django.contrib.auth import get_user_model      #devuelve el usuario activo actual
from django.db.models import F, Sum, FloatField     # para calcular el total de una orden de pedido

from inventario.models import Producto

# Create your models here.
User = get_user_model()

class Pedido(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    state = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    creater = models.CharField(max_length=20)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    updater = models.CharField(max_length=20)
    deleted = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    deleter = models.CharField(max_length=20)

    def __str__(self):
        return self.id

    @property
    def total(self):
        return self.detallepedido_set.aggregate(
            total= Sum(F("precio")*F("cantidad"), output_field=FloatField())
        )["total"]

    class Meta:
        db_table='pedido'
        ordering =['id']
        verbose_name = "pedido"
        verbose_name_plural = "pedidos"

class PedidoDetalle(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    producto= models.ForeignKey(Producto, on_delete=models.CASCADE)
    pedido= models.ForeignKey(Pedido, on_delete=models.CASCADE)
    cantidad = models.FloatField(default=1)
    state = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    creater = models.CharField(max_length=20)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    updater = models.CharField(max_length=20)
    deleted = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    deleter = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.cantidad} unidades de {self.producto.nombre}'

    
    class Meta:
        db_table='pedidoDetalles'
        ordering =['id']
        verbose_name = "pedidoDetalle"
        verbose_name_plural = "pedidoDetalles"