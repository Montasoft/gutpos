from django.shortcuts import redirect, render
from django.views.generic import View
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.http import url_has_allowed_host_and_scheme
from django.conf import settings

from carrito import carrito


#from .forms import UserRegistrerForm

# Create your views here.

class viewRegistro (View):

    def get(self, request):
        form = UserCreationForm()
        return render(request, "autenticacion/registro.html", {"form":form})

    def post(self, request):
        form= UserCreationForm(request.POST)

        if form.is_valid():
            
            usuario= form.save()
            login(request, usuario)
            return redirect('index')
        else:
            for msg in form.error_messages:
                messages.error(request, form.error_messages[msg])
            
            return render(request, "autenticacion/registro.html", {"form":form})
# status=status.HTTP_401_UNAUTHORIZED
#status=status.HTTP_201_CREATED
#status=status.HTTP_200_OK


def cerrarSesion(request):
    logout(request)
    return redirect('baseapp:index')



def log_in(request):

    if request.method=="POST":
        form=AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            usuario=form.cleaned_data.get("username")
            clave=form.cleaned_data.get("password")
            user=authenticate(request, username=usuario, password=clave)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    carritonuevo = carrito.Carrito(request)
                    messages.success(request, "Te has logueado correctamente")
                    return redirect_after_login(request)
                    return redirect('baseapp:index')
                else:
                    messages.warning(request, "Su usuario ha sido desactivado!")
                return redirect('/log_in')
            else:
                messages.error(request, "usuario o contraseña inválido")
                #for msg in form.error_messages:
                 #   messages.error(request, form.error_messages[msg])
        else:
            messages.error(request, "usuario o contraseña inválido")
            #for msg in form.error_messages:
             #   messages.error(request, form.error_messages[msg])

    form=AuthenticationForm()
    return render(request, "autenticacion/login.html", {"form":form})


def redirect_after_login(request):
    nxt = request.GET.get("next", None)
    # verifica si hay un next para redirigir despues del login.
    if nxt is None:
        return redirect(settings.LOGIN_REDIRECT_URL)
        # enviar a la pagina definida en settin para redirigir después del login
    elif not url_has_allowed_host_and_scheme(
            url=nxt,
            allowed_hosts={request.get_host()},
            require_https=request.is_secure()):
            #verificar que la dirección sea segura
        return redirect(settings.LOGIN_REDIRECT_URL)
    else:
        return redirect(nxt)
        #enviar a la página recibida en el next


def loginRecov(request):
    return "Recovery de password"