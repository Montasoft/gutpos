from django import forms
from .models import Contacto

class FormContacto(forms.ModelForm):
    class Meta:
        model = Contacto
        field = ('nombre', 'apellido', 'telefono', 'whatsapp','correo', 'PQRF', 'mensaje')
        exclude = ('state','created','creater','updated', 'updater','deleted','deleter', 'imagen')

        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control'}),
            'apellido': forms.TextInput(attrs={'class':'form-control'}),
            'telefono': forms.TextInput(attrs={'class':'form-control'}),
            'whatsapp': forms.TextInput(attrs={'class':'form-control'}),
            'correo': forms.EmailInput (attrs={'class':'form-control'}),
            'PQRF': forms.Select (attrs={'class':'form-control'}),
            'mensaje': forms.Textarea (attrs={'class':'form-control'}),
#            'imagen': forms.FileInput (),
        }
