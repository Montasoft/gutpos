
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserRegistrerForm(UserCreationForm):
    email= forms.EmailField(label='Correo electrónico', required=True)
    username= forms.CharField(label="Nombre de usuario", required=True)
    password1: forms.Field = forms.PasswordInput()
    password2: forms.Field = forms.PasswordInput()

    class Meta:
        model = User
        field = '__all__'


#class loginRecovForm(loginRecovForm)

        



