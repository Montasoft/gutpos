import datetime
from django import forms
from django.core.exceptions import ValidationError

from .models import Compra, CompraDetalles, FormaPago, PagoCompra

class FormCompra(forms.ModelForm):
    class Meta:
        model = Compra
        field = ('proveedor', 'fecha_compra', 'num_factura_proveedor', 'valor_compra', 'forma_pago', 'fecha_vence', 'fecha_recibido', 'nota')
        exclude = ('state','created','creater','updated', 'updater','deleted','deleter', 'estado')

        widgets = {
            'proveedor': forms.Select (attrs={'class':'form-control'}),
            'fecha_compra': forms.DateInput(format = '%Y-%m-%d', attrs={'type':'date'}),
            'fecha_vence': forms.DateInput(format = '%Y-%m-%d', attrs={'type':'date'}),
            'fecha_recibido': forms.DateInput(format = '%Y-%m-%d', attrs={'type':'date'}),
            #'valor_venta': forms.DecimalField (default=0.00),
            'forma_pago': forms.Select (attrs={'class':'form-control'}),
            'nota': forms.Textarea (attrs={'class':'form-control', 'row':'1'}),
        }

    def clean_fecha_compra(self):
        data =  self.cleaned_data['fecha_compra']
        if data > datetime.date.today():
            raise ValidationError(_('Fecha invalida en el futuro'))
        return data

    # TODO la siguiente función me genera error
    """
    def clean_fecha_vence(self):
        cleaned_data = super().clean()
        fecha_venta =  cleaned_data.get['fecha_venta']
        data =  cleaned_data.get['fecha_vence']
        if data < fecha_venta:
            raise ValidationError(_('Fecha invalida antes de la fecha de venta'))
        return data
    """

    def __init__(self, *args, **kwargs):
        super(FormCompra, self).__init__(*args, **kwargs)


  
class FormCompraDetalles(forms.ModelForm):
    class Meta:
        model = CompraDetalles
        field = ('compra', 'producto', 'paquetes', 'unidades',  'valor_paquete', 'descuento_pre_iva', 'descuento_pos_iva', 'iva', 'flete', 'neto','observacion')
        exclude = ('state','created','creater','updated', 'updater','deleted','deleter', 'tarifa_aplicada', 'costo')

        widgets = {
            'compra': forms.NumberInput(attrs={'type':'hidden'}),
            'producto': forms.Select (attrs={'class':'form-control'}),
            'paquetes': forms.NumberInput(attrs={'class':'form-control text-end'}),
            'unidades': forms.NumberInput(attrs={'class':'form-control text-end'}),
            'valor_paquete': forms.NumberInput (attrs={'class':'form-control text-end'}),
            'descuento_pre_iva': forms.NumberInput (attrs={'class':'form-control text-end', 'label': 'desc_pre'}),
            'iva': forms.NumberInput(attrs={'class':'form-control text-end'}),
            'flete': forms.NumberInput(attrs={'class':'form-control text-end'}),
            'neto': forms.NumberInput(attrs={'class':'form-control text-end'}),
            'observacion': forms.Textarea (attrs={'class':'form-control', 'row':'1'})
        }

class FormPagoCompra(forms.ModelForm):
     class Meta:
        model = PagoCompra
        field = ('proveedor', 'compra', 'fecha_pago', 'forma_pago', 'cajero', 'valor_pago', 'nota')
        exclude = ('state','created','creater','updated', 'updater','deleted','deleter')

        widgets = {
            'proveedor': forms.Select (attrs={'class':'form-control'}),
            'compra': forms.TextInput(attrs={'class':'form-control'}),
            'fecha_pago': forms.DateInput(format = '%Y-%m-%d', attrs={'type':'date'}),
            'forma_pago': forms.Select (attrs={'class':'form-control'}),
            'valor_pago': forms.TextInput(attrs={'class':'form-control'}),
            'cajero': forms.Select (attrs={'class':'form-control'}),
            'nota': forms.Textarea (attrs={'class':'form-control'}),
        }
        '''
        def __init__(self, *args, **kwargs):
            super(FormVenta, self).__init__(*args, **kwargs)
            self.fields['fecha_venta'].widget = widgets.AdminDateWidget()
            self.fields['fecha_vence'].widget = widgets.AdminDateWidget()
            '''    
