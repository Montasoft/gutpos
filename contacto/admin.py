from django.contrib import admin
from .models import Contacto
# Register your models here.

class ContactoAdmin(admin.ModelAdmin):
    search_fields= (['nombre', 'telefono','mensaje'])  
    list_filter=(['PQRF'])
    readonly_fields=('created', 'creater', 'updated', 'updater', 'deleted', 'deleter')

admin.site.register(Contacto, ContactoAdmin)
