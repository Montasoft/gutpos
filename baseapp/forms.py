from pyexpat import model
from socket import fromshare
from django import forms
from django.core.exceptions import ValidationError

from .models import Banco, Ciudad, Departamento, TipoDocumento, FormaPago, TipoCuentaBancaria

class FormBanco(forms.ModelForm):
    class Meta:
        model = Banco
        field = ('nombre')
        exclude = ('state','created','creater','updated', 'updater','deleted','deleter', 'estado')

class FormDepartamento(forms.ModelForm):
    class Meta:
        model = Departamento
        field = ('nombre', 'cod_dane')
        exclude = ('state','created','creater','updated', 'updater','deleted','deleter', 'estado')




