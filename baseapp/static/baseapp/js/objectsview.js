$(document).ready(function(){
    console.log("llegando a objectsview")
    let lista = document.getElementById('campos').textContent

    console.log(lista)
    for (var item in lista){
        console.log(item)

    }

})




