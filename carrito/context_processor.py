def importeTotalCarro(request):
    #variables globales
    total = 0

    if request.user.is_authenticated:
      for key, value in request.session["carrito"].items():
        total = total+(float(value["precio"]))
    else:
      total= "Debes hacer login"  

    return {"importeTotalCarro":total}            

