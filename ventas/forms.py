import datetime
from email.policy import default
from ipaddress import collapse_addresses
from time import timezone
from django import forms
from django.contrib.admin import widgets 
from .models import Producto, Venta, VentaDetalles, PagoVenta
from django.utils import timezone
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

    
class FormVenta(forms.ModelForm):
    class Meta:
        model = Venta
        field = ('id', 'cliente', 'fecha_venta', 'valor_venta', 'forma_pago','vendedor', 'nota', 'fecha_vence', 'preventa')
        exclude = ('state','created','creater','updated', 'updater','deleted','deleter', 'estado')

        widgets = {
            'cliente': forms.Select (attrs={'class':'form-control'}),
            'fecha_venta': forms.DateInput(format = '%Y-%m-%d', attrs={'type':'date'}),
            #'valor_venta': forms.DecimalField (default=0.00),
            'forma_pago': forms.Select (attrs={'class':'form-control'}),
            'vendedor': forms.Select (attrs={'class':'form-control'}),
            'nota': forms.Textarea (attrs={'class':'form-control', 'row':'1'}),
            'fecha_vence': forms.DateInput(format = '%Y-%m-%d', attrs={'type':'date'}),
            'preventa': forms.Select (attrs={'class':'form-control'}),
        }

    def clean_fecha_venta(self):
        data =  self.cleaned_data['fecha_venta']
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
        super(FormVenta, self).__init__(*args, **kwargs)



class FormVentaDetalles(forms.ModelForm):
    class Meta:
        model = VentaDetalles
        field = ('producto', 'cantidad', 'valor_unitario','descuento', 'observacion')
        exclude = ('state','created','creater','updated', 'updater','deleted','deleter', 'tarifa_aplicada', 'costo', 'iva', 'neto')

        widgets = {
            'venta': forms.NumberInput(attrs={'type':'hidden'}),
            'producto': forms.Select (attrs={'class':'form-control', 'tabIndex': '7'}),
            'cantidad': forms.NumberInput(attrs={'class':'form-control text-end', 'tabIndex': '3'}),
            'valor_unitario': forms.NumberInput (attrs={'class':'form-control text-end', 'tabIndex': '4'}),
            'descuento': forms.NumberInput (attrs={'class':'form-control text-end', 'tabIndex': '5'}),
            'observacion': forms.Textarea (attrs={'class':'form-control', 'row':'1', 'tabIndex': '6'}),
        }

class FormPagoVenta(forms.ModelForm):
     class Meta:
        model = PagoVenta
        field = ('cliente', 'venta', 'fecha_pago', 'forma_pago', 'cajero', 'valor_pago', 'nota')
        exclude = ('state','created','creater','updated', 'updater','deleted','deleter')

        widgets = {
            'cliente': forms.Select (attrs={'class':'form-control'}),
            'venta': forms.TextInput(attrs={'class':'form-control'}),
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
