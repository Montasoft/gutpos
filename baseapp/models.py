from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone, dateformat
from django.utils.translation import gettext as _
from django.db import models
from django.db.models import F, Sum, FloatField     # para calcular el total de una orden de pedido


class BaseModel(models.Model):
    state = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now=False, auto_now_add=True, null=True, blank=True)
    creater = models.CharField(max_length=30, null=True, blank=True)
    updated = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True )
    updater = models.CharField(max_length=30, null=True, blank=True)
    deleted = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    deleter = models.CharField(max_length=30, null=True, blank=True)

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
        abstract = True  

    def save(self, *args, **kwargs):
        ''' Al guardar actualizar fecha y usuario del registro 
            se recibe el usuario en el campo de updater
            pero si es registro nuevo se guardará en creater '''
        
        if not self.pk: # Si es un nuevo registro
            self.creater = self.updater
            self.updater = None
        else:   # Si es una actualización
            print( "save - update")
            self.updated = timezone.now()
            self.updater = self.updater

        return super(BaseModel, self).save(*args, **kwargs)

#######################################################################################
class Menu(models.Model):
    nombre = models.CharField(max_length=50)
    orden = models.IntegerField()
    icono = models.CharField(max_length=50)

    class Meta:
        ordering =['orden']
        verbose_name = "Menú"
        verbose_name_plural = "Menús"

    def __str__(self):
        return  self.nombre
    
    
#######################################################################################
class SubMenu(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    nombre = models.CharField(_("nombre"), max_length=50)
    orden = models.IntegerField()
    icono = models.CharField(max_length=50)
    enlace = models.CharField(max_length=128)
    favorito = models.BooleanField(default=False)
    variable = models.CharField(max_length=20)

    class Meta:
        ordering =['orden']
        verbose_name = "Submenú"
        verbose_name_plural = "submenús"

    def __str__(self):
        return  self.nombre


#######################################################################################
class Departamento(models.Model):
    nombre = models.CharField(max_length=50)
    cod_dane = models.CharField(max_length=2, unique=True)
    
    class Meta:
        ordering =['nombre']
        verbose_name = "Departamento"
        verbose_name_plural = "Departamentos"

    def __str__(self):
        return self.nombre
        
    def get_absolute_url(self):
        return reverse('baseapp:departamentodetail', kwargs={'pk' :self.id})

#######################################################################################
class Ciudad(BaseModel):
    nombre = models.CharField(max_length=150)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)
    cod_dane = models.CharField(max_length=5, unique=True)

    class Meta:
        ordering =['nombre']
        verbose_name = "Ciudad"
        verbose_name_plural = "Ciudades"

    def __str__(self):
        return  self.nombre
    
    def get_absolute_url(self):
        return reverse('baseapp:ciudaddetail', kwargs={'pk' :self.id})

#######################################################################################
class TipoDocumento(BaseModel):
    cod = models.CharField(max_length=30)
    nombre = models.CharField(max_length=150)

    class Meta:
        ordering =['nombre']
        verbose_name = "Tipo de Documento"
        verbose_name_plural = "Tipos de documento"

    def __str__(self):
        return  self.nombre
    
    def get_absolute_url(self):
        return reverse('baseapp:tipodocumentodetail', kwargs={'pk' :self.id})


#######################################################################################
class FormaPago(BaseModel):
    nombre = models.CharField(max_length=30)
    descripcion = models.CharField(max_length=150)

    class Meta:
        ordering =['nombre']
        verbose_name = "Forma de Pago"
        verbose_name_plural = "Formas de Pago"

    def __str__(self):
        return  self.nombre
    
    def get_absolute_url(self):
        return reverse('baseapp:formapagodetail', kwargs={'pk' :self.id})


#######################################################################################
class Tercero(BaseModel):
    nombre = models.CharField(max_length=150)
    tipo_documento = models.ForeignKey(TipoDocumento, on_delete=models.CASCADE, null=True, blank=True)
    numero_documento = models.CharField(max_length=20, null=True, blank=True)
    ciudad = models.ForeignKey(Ciudad, on_delete=models.CASCADE, null=True, blank=True)
    direccion = models.CharField(max_length=150, null=True, blank=True)
    barrio = models.CharField(max_length=150, null=True, blank=True)
    ubicacion_GPS = models.CharField(max_length=50, null=True, blank=True)
    telefono = models.CharField(max_length=10, null=True, blank=True)
    whatsapp = models.CharField(max_length=10, null=True, blank=True)
    email = models.EmailField()

    class Meta:
        abstract = True


#######################################################################################
class TipoCuentaBancaria(models.Model):
    nombre = models.CharField(max_length=30)

    class Meta:
        ordering =['nombre']
        verbose_name = "Tipo de Cuenta Bancaria"
        verbose_name_plural = "Tipos de cuenta bancaria"

    def __str__(self):
        return  self.nombre
    
    def get_absolute_url(self):
        return reverse('baseapp:tipocuentabancaria', kwargs={'pk' :self.id})


#######################################################################################
class Banco(BaseModel):
    nombre= models.CharField(max_length=150)

    def __str__(self):
        return  self.nombre
    
    def get_absolute_url(self):
        return reverse('baseapp:bancodetail', kwargs={'pk' :self.id})
    
    class Meta:
        ordering =['nombre']
        verbose_name = "Banco"
        verbose_name_plural = "Bancos"

    