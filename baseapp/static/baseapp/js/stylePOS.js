
$(document).ready(function(){
    // Tomar los datos recibidos desde el back en el elemento opcionesmenu
    var jsonMenu = JSON.parse(document.getElementById('opcionesmenu').textContent)

    console.log (jsonMenu)
    let menuDinamico = document.getElementById('menuDinamico');

    menuLocalS = JSON.parse(localStorage.getItem('menu'));
    ajaxPedirMenu() //comentar esta linea cuando ya este el menu definido para no pedirlo cada vez
    if (menuLocalS){
        console.log("hay menu")
        PintarMenu()
    }else{
        console.log("pedir menu")
        ajaxPedirMenu()
    }

})

//######################################################################################
//######################################################################################

function ajaxPedirMenu(){
    console.log("ajaxPedirMenu.28")
    
    //TODO

    // asignar el número de la venta activa.
//    document.getElementById('id_venta').value = document.getElementById('venta').value
      
    $.ajax({
        url: '../pedirMenu',
        type: "GET",
        data: $({'Venta': 8}).serialize(),
        success: function(data) {
            if (data['success']) {
                // proceso retorna con exito
                console.log("success")            
                
                // guardar los datos del menu en el LocalStorage
                localStorage.setItem('menu', JSON.stringify(data['menu']))
  
            }
            else {
                // Here you can show the user a success message or do whatever you need
                console.log("error")
                $(formVenta).find('.success-message').show();
            }
        },
        error: function () {
            $(formVenta).find('.error-message').show()
        }
    });
  }
  

//######################################################################################
function PintarMenu(){
    // recoparar los datos del LocalStorage para la llave 'menu'
    jsonMenu = JSON.parse(localStorage.getItem('menu'));
    console.log("pintarmenu")
    console.log(jsonMenu)
    //recorrer el json
    for (grupo of jsonMenu){
        // agregar cada grupo de opciones al menu    
        let txthtml = '<a href="#' + grupo.nombre + '" data-toggle="collapse" aria-expanded="false" class="dropdown-toggle">'
        txthtml += "<i class='"+ grupo.icono +"' aria-hidden='true' title='"+ grupo.nombre +"'></i>"
        txthtml += '<span> ' + grupo.nombre + '</span></a>'
        txthtml += '<ul class="collapse list-unstyled" id="'+grupo.nombre+ '"></ul>'

        menuDinamico.insertAdjacentHTML('beforeend', txthtml)
        let submenu = document.getElementById(grupo.nombre);
        // recorrer la lista de opciones submenu para cada grupo de menu
        for (opc of grupo.submenu){
                
            let llaves =  '{% if request.path == "' + opc.enlace  + '" %} active {% endif %}'
            
            txthtml = "<a class='" + llaves + "'" 
            txthtml += "href='" + opc.enlace + "'>"
            txthtml += "<div class= 'option'>" 
            txthtml += "<i class='"+ opc.icono +"' aria-hidden='true' title='"+ opc.nombre +"'></i>"
            txthtml += "<h6>"+ opc.nombre +"</h6>"
            txthtml += "</div>"
            txthtml += "</a>"
            
            console.log(txthtml)
            submenu.insertAdjacentHTML('beforeend', txthtml)
        }
    }
}




// ejecutar funci{on en el evento click

document.getElementById("btn_open").addEventListener("click", open_close_menu);

//declaramos variables
var side_menu = document.getElementById("menu__side");
var btn_open = document.getElementById("btn_open");
var body = document.getElementById("body");
var footer = document.getElementById("footer");


//evento para mostrar y ocultar el menu

    function open_close_menu(){
        /* toggle adiciona y quita la clase con cada peticion*/

        body.classList.toggle("body_move");
        side_menu.classList.toggle("menu__side_move");
        footer.classList.toggle("menu__side_move");
    }

// si el ancho de la página es menor a 760px, ocultará el menú al recargar la página

if (window.innerWidth > 760){
    body.classList.add("body_move");
    side_menu.classList.add("menu__side_move");
    footer.classList.add("menu__side_move");

}

//haciendo el menu responsive (adaptable)

window.addEventListener("resize", function(){

    if  (window.innerWidth > 760){
        body.classList.remove("body_move");
        side_menu.classList.remove("menu__side_move");
        footer.classList.remove("menu__side_move");
    }

    if  (window.innerWidth < 760){
        body.classList.add("body_move");
        side_menu.classList.add("menu__side_move");
        footer.classList.add("menu__side_move");
    }
})