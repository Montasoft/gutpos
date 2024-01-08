from django.shortcuts import redirect, render, HttpResponse

from .forms import FormContacto

from django.core.mail import EmailMessage
# otra alternativa es con send_mail

# Create your views here.

def contacto(request):
    formContacto = FormContacto() 

    if request.method =="POST":
        print("dentro del post")
        print(request.POST)
        formContacto=FormContacto(data=request.POST) 
        print(formContacto.is_valid())
        if formContacto.is_valid():
            print("dentro del valid")
            nombre = request.POST.get("nombre")
            apellido = request.POST.get("apellido")
            telefono = request.POST.get("telefono")
            whatsapp = request.POST.get("whatsapp")
            correo = request.POST.get("correo")
            PQRF = request.POST.get("PQRF")
            mensaje = request.POST.get("mensaje")
            #imagen = request.FILES["imagen"]
            print(nombre, " ", apellido, " ", telefono, " ", whatsapp, " ", correo, " ",PQRF, " ",mensaje, " ")

            email = EmailMessage("Mensaje desde Django", "el usuario de nombre:  {} con la dirección {} escibe lo siguiente: \n\n {}" .format(nombre, correo, mensaje),"soporte@solcatsas.com",["papeleria5613837@gmail.com"], reply_to=[correo] )
            
            try:
                email.send()
                return redirect("/contacto/?valido")
            except:
                return redirect("/contacto/?errorDeEnvio")

    return render(request, "contacto/contacto.html", {'form':formContacto})
    
    