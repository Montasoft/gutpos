
let codIngresado = document.getElementById("codIngresado");
let id_produto = document.getElementById("id_produto");
let id_paquetes = document.getElementById("id_paquetes");
let id_unidades = document.getElementById("id_unidades");
let id_valor_paquete = document.getElementById("id_valor_paquete");
let id_valorUnitario = document.getElementById("id_valorUnitario");
let id_neto = document.getElementById("id_neto");
let id_descuento_pre_iva = document.getElementById("id_descuento_pre_iva");
let id_iva = document.getElementById("id_iva");
let id_descuento_pos_iva = document.getElementById("id_descuento_pos_iva");
let id_flete = document.getElementById("id_flete");

// funcion a ejecutar cuando la pagina haya sido cargada.
$(document).ready(function () {
  console.log("ready!");

  document.getElementById("id_unidades").oninput = calcularNeto;
  document.getElementById("id_paquetes").oninput = calcularNeto;
  document.getElementById("id_valor_paquete").oninput = calcularNeto;
  document.getElementById("id_valorUnitario").oninput = hallarValorPaquete;
  document.getElementById("id_neto").oninput = calcularNeto;
  document.getElementById("id_descuento_pre_iva").oninput = calcularNeto;
  document.getElementById("id_iva").oninput = calcularNeto;
  document.getElementById("id_descuento_pos_iva").oninput = calcularNeto;
  document.getElementById("id_flete").oninput = calcularNeto;
  document.getElementById("codIngresado").onchange = traerDAtosDelLocalStorage;
  $(document.getElementsByName("observacion")).attr("rows", "1");


  //FUCCION PARA AGREGAR EVENTON A LOS BOTONES DE ELIMINAR DETALLES DE COMPRA
  var botonEliminar = document.getElementsByClassName("eliminar");
  for (var i = 0; i < botonEliminar.length; i++) {
    // Añadimos un event listener a cada elemento
    botonEliminar[i].addEventListener("click", function () {

      var boton = this;
      //agregar la funcion para eliminar registro a cada botón
      eliminarDetalledeCompra(this.dataset.idDetalle, function(resultado) {
      if (resultado === 'success') {
        // si el regisro fue eliminado ocultar la fila
        var fila = boton.parentNode.parentNode; 
        fila.style.display = 'none';
      }
    });
  });
}

  // document.getElementById('codIngresado').onblur = traerDAtosDelLocalStorage
  codIngresado.addEventListener("blur", function () {
    traerDAtosDelLocalStorage();
  });

  document.getElementById("final").scrollIntoView(true);
  scrollTabla();

  cargarDatosALocalStorage(); // carga la lista de productos


  $(".select").select2();

  $("#id_observacion").blur(function () {
    document.getElementById("btnAdd").focus(); //pasar el foco a btnAdd
  });

  // Llamar a la función al cargar la página y cuando cambie el tamaño de la ventana
  ajustarTamanioTexto();
  $(window).resize(ajustarTamanioTexto);
});

//FUNCION  PARA OBTENER LA CLAVE csrftoken ***************************************
function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
          var cookie = jQuery.trim(cookies[i]);
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}// ******************************************************************************

function eliminarDetalledeCompra(id_eliminar, callback) { //*********************

  console.log(id_eliminar)

  // Mostrar un cuadro de diálogo de confirmación
  Swal.fire({
    title: '¿Estás seguro?',
    text: '¡No podrás revertir esto!',
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#3085d6',
    cancelButtonColor: '#d33',
    confirmButtonText: 'Sí, eliminarlo!'
  }).then((result) => {
    if (result.isConfirmed) {
        // Si el usuario confirma, enviar la solicitud de eliminación
        // usando AJAX
        let csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
        var csrftoken = getCookie('csrftoken');
        $.ajax({
            url: '../eliminarDetalleCompra/', // La URL de tu vista en Django
            type: 'POST',
            data: {
                csrfmiddlewaretoken : csrftoken,
                'id': id_eliminar, // Pasar el ID del registro a eliminar
                'csrf_token': csrfToken // Necesario para la protección CSRF en Django
                
            },
              success: function(response) {
                // Manejar la respuesta del servidor
                if (response.success) {
                    // Si la eliminación fue exitosa, mostrar un mensaje
                    Swal.fire(
                        '¡Eliminado!',
                        'El registro ha sido eliminado.',
                        'success'
                    );
                    callback('success'); // Devolver el reporte de exito
                } else {
                    // Si hubo un error al eliminar, mostrar un mensaje de error
                    Swal.fire(
                        'Error',
                        'Hubo un error al intentar eliminar el registro.',
                        'error'
                    );
                    callback('error');  // devolver el reporte de error
                }
            }
        });
    }
  });
} // *****************************************************************************

function calcularNeto() {
  let paquetes = Number(id_paquetes.value ?? 1);
  let unidades = Number(id_unidades.value ?? 1);
  let valorPaquete = Number(id_valor_paquete.value ?? 0);
  let valUnidad = Number(id_valorUnitario.value ?? 0);
  let neto = id_neto.value ?? 0;
  let descuento_pre_iva = Number(id_descuento_pre_iva.value ?? 0);
  let iva = Number(id_iva.value ?? 0);
  let des_pos_iva = Number(id_descuento_pos_iva.value ?? 0);
  let flete = Number(id_flete.value ?? 0);
  let val_des_ant_iva = (valorPaquete * descuento_pre_iva) / 100;
  let descontado1 = [valorPaquete] - [val_des_ant_iva];
  let val_iva = ([descontado1] * [iva]) / 100;
  let val_des_pos_iva = ([descontado1] * [des_pos_iva]) / 100;
  let descontado2 = [descontado1] - [val_des_pos_iva];
  let val_flete = ((descontado2 + val_iva) * flete) / 100;
  let val_neto_emp = [descontado2] + [val_iva] + [val_flete];
  let val_neto_unid = [val_neto_emp] / [unidades];

  let Totaldelinea =
    (Number(descontado1) +
      Number(val_iva) -
      Number(val_des_pos_iva) +
      Number(val_flete)) *
    Number(paquetes);

  //id_neto.value = (((([valorPaquete.value ?? 1]-([valorPaquete.value ?? 1]*([descuento_pre_iva.value ?? 0])/100))+([valorPaquete.value ?? 1]*[iva.value ?? 0]/100))+([valorPaquete.value ?? 1]*[flete.value ?? 0]/100))/[unidades.value ?? 1])
  id_neto.value = Math.round((Totaldelinea + Number.EPSILON) * 100) / 100;
  id_valorUnitario.value =
    Number(id_valor_paquete.value) / Number(id_unidades.value);
}

function hallarValorPaquete() {
  id_valor_paquete.value =  Number(id_valorUnitario.value) * Number(id_unidades.value);
  calcularNeto();
}
// Función para ajustar el tamaño del texto del input
function ajustarTamanioTexto() {
  var containerWidth = $("#div_total").width();
  var inputWidth = $("#totalcompra").width();

  // Si el tamaño del contenedor es menor que el del input, reducir el tamaño de fuente
  if (containerWidth < inputWidth + 6) {
    var nuevoTamanio = containerWidth / 8; // Puedes ajustar este valor según tus necesidades
    $("#totalcompra").css("font-size", nuevoTamanio + "px");
  } else {
    // Restaurar el tamaño de fuente predeterminado si el contenedor es lo suficientemente grande
    $("#myInput").css("font-size", "");
  }
}

function cargarDatosALocalStorage() {
  //cargar lista de productos al local storage
  var jsonProductos = JSON.parse(
    document.getElementById("productos").textContent
  );
  console.log(jsonProductos);
  for (let producto of jsonProductos) {
    localStorage.setItem(producto.id, JSON.stringify(producto));
  }

  for (let i = 0; i < localStorage.length; i++) {
    let key = localStorage.key(i);
    // console.log(`${key}: ${localStorage.getItem(key)}`);
    let thisproduc = JSON.parse(localStorage.getItem(key));
    //  console.log(thisproduc.nombre)
  }
} // FIN DE cargarDatosALocalStorage********************************************************

function traerDAtosDelLocalStorage() {
  //para traer a pantalla el nombre del producto despues de ingresar el codigo
  var codIngresado = document.getElementById("codIngresado").value;

  prod = JSON.parse(localStorage.getItem(codIngresado)); // traer datos del producto en formato json

  //mostrar cada valor en su campo
  document.getElementById("id_producto").value = prod.id;
  document.getElementById("codIngresado").value = prod.id;
  document.getElementById("id_paquetes").value = 1;
  document.getElementById("id_unidades").value = prod.cantidad_x_empaque;
  document.getElementById("id_valor_paquete").value =
    prod.costo * prod.cantidad_x_empaque;
  document.getElementById("id_neto").value = prod.costo;
  id_valorUnitario.value = Number(id_valor_paquete.value) / Number(id_unidades.value);
  document.getElementById("btnAdd").focus();
}

function ajaxValidarCompraDetalle() {
  let formCompraDetalle = "#formCompraDetalle";
  let total = document.getElementById("totalCompra");
  console.log("ajaxValidarCompraDetalle");

  // asignar el número de la compra activa.
  document.getElementById("id_compra").value = document.getElementById("compra").value;

  console.log($(formCompraDetalle).serialize());

  var url_post = $("#formCompraDetalle").data("post-url");
  $.ajax({
    url: url_post,
    type: "POST",
    data: $(formCompraDetalle).serialize(),
    success: function (data) {
      if (data["success"]) {
        // proceso retorna con exito
        console.log("success");

        //tomo los datos para mostrarlo en la tabla
        addRowTable(data["detalleCreado"]);

        total.value = data["detalleCreado"].total_compra;

        //desplazo el scroll para mostra el ultimo registro
        scrollTabla();
        document.getElementById("formCompraDetalle").reset();
        document.getElementById("codIngresado").focus();
      } else {
        // Here you can show the user a success message or do whatever you need
        console.log("error");

        $(formCompra).find(".success-message").show();

        // Mostrar los errores en pantalla
        var errores = JSON.parse(data.errors);
        for (var campo in errores) {
          // Mostrar los errores de cada campo en tu formulario
          var mensajeError = errores[campo][0].message;
          console.log(mensajeError);
          // Muestra mensajeError en el campo correspondiente o en algún otro lugar de tu página
        }
      }
    },
    error: function () {
      $(formCompra).find(".error-message").show();
    },
  });
}

function scrollTabla() {
  var tabla = document.getElementById("tCompraDetalles");
  // TODO Medir el scroll y dar la medida excacta
  tabla.scrollTop = "9999";
}

function cerrarModal() {
  alert("cerrarModal");
  $("#modal").modal("hide");
}
function registrarPago() {
  alert("Registrar pago");
}

function AjaxGetOptionSelect() {
  /*pedir mediante ajax las opciones para llenar los select de form */
  $.ajax({
    url: "AjaxGetOptionSelect",
    type: "POST",
    data: $(formCompra).serialize(),
    success: function (response) {
      console.log("response", response);
      let responseJson = response;

      if (responseJson.Generado) {
        if (responseJson.Generado[0].produc_json) {
          for (var prod of Object.values(
            responseJson.Generado[0].produc_json
          )) {
            // Cargar la lista de opciones del select de productos.
            op =
              "<option value= '" + prod.id + "' > " + prod.text + "</option>";
            document.getElementById("cliente").innerHTML += op;
          }
        }
        if (responseJson.Generado[0].client_json) {
          for (var cli of Object.values(responseJson.Generado[0].client_json)) {
            // Cargar la lista de opciones del select de clientes.
            op = "<option value= '" + cli.id + "' > " + cli.text + "</option>";
            document.getElementById("cliente").innerHTML += op;
          }
        }
      } else {
        err = responseJson.error;
        motrar = "Error: " + err;
        console.log("mostrar ", mostrar);
      }
    },
    error: function (error) {
      console.log(error);
    },
  });
}

function addRowTable(data) {
  //mostrar la lista de los productos ya incluidos en la compra
  console.log(data);

  // Objeto principal que contiene otros objetos como valores
  var mainObject = JSON.parse(data);

  // Recorrer el objeto principal
  for (var key in mainObject) {
    // Verificar si la clave es propia del objeto y no heredada
    if (mainObject.hasOwnProperty(key)) {
      // Acceder al objeto interno a través de la clave y recorrerlo
      var innerObject = mainObject[key];
      for (var innerKey in innerObject) {
        if (innerObject.hasOwnProperty(innerKey)) {
          console.log("Inner Key:", innerKey, "Value:", innerObject[innerKey]);
          //si encuentra el diccionario de fields toma los valores
          if (innerKey == "fields") {
            prod = JSON.parse(
              localStorage.getItem(innerObject["fields"]["producto"])
            );

            console.log("paquetes", innerObject["fields"]["paquetes"]);
            console.log("id", innerObject["pk"]);
            id = innerObject["pk"];
            compra = innerObject["fields"]["compra"];
            codBar = prod.id;
            nombre = prod.nombre;
            paquetes = Number.parseFloat(innerObject["fields"]["paquetes"]).toFixed(2);
            unidades = Number.parseFloat(innerObject["fields"]["unidades"]).toFixed(2);
            valorPaquete = Number.parseFloat(innerObject["fields"]["valor_paquete"]).toFixed(2);
            descPreIva = Number.parseFloat(innerObject["fields"]["descuento_pre_iva"]).toFixed(2);
            descPosIva = Number.parseFloat(innerObject["fields"]["descuento_pos_iva"]).toFixed(2);
            iva = Number.parseFloat(innerObject["fields"]["iva"]).toFixed(2);
            flete = Number.parseFloat(innerObject["fields"]["flete"]).toFixed(2);
            neto = Number.parseFloat(innerObject["fields"]["neto"]).toFixed(2);
            if (innerObject["fields"]["observacion"] == null) {
              obse = "";
            } else {
              obse = innerObject["fields"]["observacion"];
            }
            //  btnEditar  = "<a href='''{% url 'compras:eliminarDetalleCompra' x.id %}''' class = '' ><i class='fas fa-pen'></i>"
            btnEditar = "<button type='button'  data-bs-toggle='modal' data-bs-target='#modal_pago'><i class='fas fa-pen' aria-hidden='true'></i></button>";
            btnEditar = "<button type='button'  data-bs-toggle='modal' data-bs-target='#modal_pago' class = 'btn btn-primary btn-sm' style= 'width=35px;'><i class='fas fa-pen' aria-hidden='true'></i></button>";
            //btnElimiar ="<a href='''{% url 'compras:eliminarDetalleCompra' x.id %}''' class = '' data-idEliminar='{{x.id}}' ><i class='fas fa-trash-alt'></i>";
            btnElimiar ="<a href='' class = 'eliminar' data-id-detalle='{{x.id}}' ><i class='fas fa-trash-alt'></i>";
            btns = btnElimiar;

            tdtd = "</td><td>";
            tdtd_r = "</td><td class='text-end'>";

            //TODO Mostrar datos resumen

            var fila ="<tr><th scope='row'> " +id +"</th><td>" + codBar +  tdtd + nombre + tdtd + paquetes + tdtd + unidades + tdtd + valorPaquete + tdtd_r + descPreIva + tdtd_r + iva + tdtd_r + descPosIva + tdtd_r + flete + tdtd_r + neto + tdtd_r + obse + tdtd + btns + "</td></tr>";

            console.log(fila);
            let ntr = document.createElement("TR");
            ntr.innerHTML = fila;
            //let tabla = document.getElementById('tb_compraDetalles')
            document.getElementById("tb_compraDetalles").appendChild(ntr);
            //tabla.appendChild(ntr);
          }
        }
      }
    }
  }
};
//const ventaa = JSON.parse(document.getElementById('datoss').textContent);
