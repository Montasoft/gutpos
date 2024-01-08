from django.contrib import admin

from pedidos.models import Pedido, PedidoDetalle
# Register your models here.

class pedidoAdmin(admin.ModelAdmin):
    list_display = (['user', 'created'])  
    search_fields= (['user', 'created'])  
    list_filter=(['user'])
    readonly_fields=('created', 'creater', 'updated', 'updater', 'deleted', 'deleter')

class pedidoDetalleAdmin(admin.ModelAdmin):
    list_display = (['pedido_id', 'producto_id', 'cantidad'])  
    search_fields= (['pedido_id', 'created'])  
    list_filter=(['pedido_id'])
    readonly_fields=('created', 'creater', 'updated', 'updater', 'deleted', 'deleter')


admin.site.register(Pedido, pedidoAdmin)
admin.site.register(PedidoDetalle, pedidoDetalleAdmin)



