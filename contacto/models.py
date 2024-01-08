from email.policy import default
from mailbox import NoSuchMailboxError
from django.db import models

# Create your models here.

PQRF_choices= (('P', 'Petición'),('Q', 'Queja'),('R', 'Reclamo'),('F', 'Felicitaciones'))

class Contacto(models.Model):
    nombre= models.CharField(max_length=100)
    apellido= models.CharField(max_length=100)
    telefono= models.CharField(max_length=100)
    whatsapp= models.CharField(max_length=100)
    correo= models.EmailField(max_length=100)
    PQRF = models.CharField(choices= PQRF_choices, max_length=1, default= "F")
    mensaje= models.TextField(max_length=1000)
    imagen = models.FileField(upload_to='PQRF')

    state = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    creater = models.CharField(max_length=20)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    updater = models.CharField(max_length=20)
    deleted = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    deleter = models.CharField(max_length=20)
