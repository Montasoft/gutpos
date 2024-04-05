from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone, dateformat
from django.utils.translation import gettext as _
from django.db.models import F, Sum, FloatField     # para calcular el total de una orden de pedido
from baseapp.models import BaseModel
from django.views import generic


#######################################################################################
class Categoria(BaseModel):
    nombre= models.CharField(max_length=50)
    descripcion = models.CharField(max_length=150, null=True, blank=True)
    
    class Meta:
        ordering =['nombre']
        verbose_name = "categoria de productos"
        verbose_name_plural = "categorias de Productos"

    def __str__(self):
        return  self.nombre
    
    def get_absolute_url(self):
        return reverse('inventario:categoriadetail', kwargs={'pk' :self.id})
        
 
####################################################################################### 
class SubCategoria(BaseModel):
    nombre = models.CharField(_('nombre'), max_length=50)
    descripcion = models.CharField(_('descripcion'), max_length=150, null=True, blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name = 'subcategoria')

    class Meta:
        ordering =['nombre']
        verbose_name = "Sub categoria de productos"
        verbose_name_plural = "Sub categorias de Productos"

    def __str__(self):
        return f'categoria: {self.categoria.nombre} - Subcategoría  {self.nombre}'

    def get_absolute_url(self):
        return reverse('inventario:subcategoriadetail', kwargs={'pk' :self.id})


#######################################################################################
class EstadoProducto(BaseModel):
    nombre = models.CharField(max_length=20)
    descripcion = models.CharField(max_length=150)

    class Meta:
        ordering =['nombre']
        verbose_name = "Estado del producto"
        verbose_name_plural = "Estados de productos"


    def __str__(self):
        return  self.nombre
    
    def get_absolute_url(self):
        return reverse('inventario:estadoproductodetail', kwargs={'pk' :self.id})



#######################################################################################
class Producto(BaseModel):
    nombre= models.CharField(max_length=100)
    codigo_barras = models.CharField(max_length=24, null=True, blank=True, unique=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    subcategoria = models.ForeignKey(SubCategoria, on_delete=models.CASCADE)
    costo = models.FloatField()
    precio_venta = models.FloatField()
    precio_mayor = models.FloatField(null = True, blank = True)
    iva = models.IntegerField(default=0)
    existencias = models.FloatField()
    estado = models.ForeignKey(EstadoProducto, on_delete=models.CASCADE)
    dim_Alto  = models.FloatField(null = True, blank = True)
    dim_Ancho = models.FloatField(null = True, blank = True)
    dim_fondo = models.FloatField(null = True, blank = True)
    peso = models.FloatField(null = True, blank = True)
    Nota =models.CharField(max_length=200, null = True, blank = True)
    descripcion = models.CharField(max_length=528, null = True, blank = True)
    cantidad_x_empaque = models.FloatField(default=1, null = True, blank = True)
    imagen = models.ImageField(upload_to='productos', null = True, blank = True)

    class Meta:
        ordering =['nombre']
        verbose_name = "producto"
        verbose_name_plural = "productos"

    def __str__(self):
        return str(self.nombre)
    
    def get_absolute_url(self): 
        return reverse('inventario:producto', kwargs={'pk' :self.id})
