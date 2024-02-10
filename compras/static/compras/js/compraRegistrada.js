var codIngresadoInput = document.getElementById('codIngresado');
var productoSelect = document.getElementById('id_produto');
let paquetes = document.getElementById('id_paquetes')
let unidades = document.getElementById('id_unidades')
let valPaq = document.getElementById('id_valor_paquete')
var neto = document.getElementById('id_neto')
  
//TODO configurar el modal para editar el detalle de la venta
//TODO Configurar la tabla para mostrar los detales de la venta
$(document).ready(function() {
  console.log("ready!");
  
  
  $(document.getElementsByName('observacion')).attr('rows', '1');               
  document.getElementById('final').scrollIntoView(true)
  scrollTabla()

  cargarDatosALocalStorage() // carga la lista de productos
  
  codIngresadoInput.addEventListener('blur', function() {
    // Este código se ejecutará justo antes de que el elemento pierda el foco
    traerDAtosDelLocalStorage()
  })



  paquetes.addEventListener('input', function(){
    //al digitar la cantida de paquetes llamar calcular valor neto
    console.log('calcular neto paquete')

    calcularNeto()
  })

  unidades.addEventListener('input', function(){
    //al digitar la cantida de paquetes llamar calcular valor neto
    console.log('calcular neto uniades')
    calcularNeto()
  })

  valPaq.addEventListener('input', function(){
      calcularNeto()
  })
  



  $("#id_observacion").blur(function(){
    document.getElementById("btnAdd").focus(); //pasar el foco a btnAdd
});

  
// Función para ajustar el tamaño del texto del input
function ajustarTamanioTexto() {
  var containerWidth = $('#div_total').width();
  var inputWidth = $('#totalcompra').width();
  
  // Si el tamaño del contenedor es menor que el del input, reducir el tamaño de fuente
  if (containerWidth < (inputWidth+6)) {
      var nuevoTamanio = containerWidth / 8;  // Puedes ajustar este valor según tus necesidades
      $('#totalcompra').css('font-size', nuevoTamanio + 'px');
  } else {
      // Restaurar el tamaño de fuente predeterminado si el contenedor es lo suficientemente grande
      $('#myInput').css('font-size', '');
  }
}

// Llamar a la función al cargar la página y cuando cambie el tamaño de la ventana
ajustarTamanioTexto();
$(window).resize(ajustarTamanioTexto);
});


function cargarDatosALocalStorage(){
    //cargar lista de productos al local storage
    var jsonProductos = JSON.parse(document.getElementById('productos').textContent)
    console.log(jsonProductos)
    for (let producto of jsonProductos){

      localStorage.setItem(producto.id, JSON.stringify(producto));  
    }
    
    for(let i=0; i<localStorage.length; i++) {
      let key = localStorage.key(i);
//      console.log(`${key}: ${localStorage.getItem(key)}`);
      let thisproduc =JSON.parse(localStorage.getItem(key))
  //    console.log(thisproduc.nombre)
    }
} // FIN DE cargarDatosALocalStorage********************************************************


function traerDAtosDelLocalStorage(){
  //para traer a pantalla el nombre del producto despues de ingresar el codigo
  var codIngresado = document.getElementById("codIngresado").value;

  console.log("codIngresado: ", codIngresado);
  prod = JSON.parse(localStorage.getItem(codIngresado));
  console.log(prod)
  
  console.log(prod.nombre, "  desde traer nombre");
  
  document.getElementById("id_producto").value = prod.id;
  document.getElementById("codIngresado").value = prod.id;
  document.getElementById("id_paquetes").value = 1;
  document.getElementById("id_unidades").value = prod.cantidad_x_empaque;
  document.getElementById("id_valor_paquete").value = (prod.costo * prod.cantidad_x_empaque);
  document.getElementById("id_neto").value = prod.costo;
  document.getElementById("btnAdd").focus();
}

function calcularNeto(){
  console.log(paquetes.value * unidades.value )
  //=(((([Val_Uni_compra]-([Val_Uni_compra]*Nz([des_ant_iva])/100))+([Val_Uni_compra]*[IVA]/100))+([Val_Uni_compra]*[flete]/100))/[uni_emp])

  neto.value = ((valPaq.value ?? 1) * (paquetes.value ?? 1))
};

function ajaxValidarCompraDetalle(){
  let formCompraDetalle = '#formCompraDetalle';
  let total = document.getElementById('totalCompra')
  console.log("ajaxValidarCompraDetalle")
  
  // asignar el número de la compra activa.
  document.getElementById('id_compra').value = document.getElementById('compra').value

  console.log($(formCompraDetalle).serialize())
  
  var url_post = $("#formCompraDetalle").data("post-url");
  $.ajax({
      url: url_post,
      type: "POST",
      data: $(formCompraDetalle).serialize(),
      success: function(data) {
          if (data['success']) {
              // proceso retorna con exito
              console.log("success")            
              
              //tomo los datos para mostrarlo en la tabla
              let datos = []
              datos.push(data['detalleCreado'])
              addRowTable(datos)

              total.value =(data['detalleCreado'].total_compra)

              //desplazo el scroll para mostra el ultimo registro
              scrollTabla()
              document.getElementById('formCompraDetalle').reset()
              document.getElementById('codIngresado').focus() 
          }
          else {
              // Here you can show the user a success message or do whatever you need
              console.log("error")
              $(formCompra).find('.success-message').show();
          }
      },
      error: function () {
          $(formCompra).find('.error-message').show()
      }
  });
}

function scrollTabla(){
  var tabla = document.getElementById('tCompraDetalles');
  // TODO Medir el scroll y dar la medida excacta
  tabla.scrollTop = '9999'; 
}

function cerrarModal(){
  alert("cerrarModal")
  $('#modal').modal('hide');
}
function registrarPago(){
  alert("Registrar pago")
}
/*
$(function(){
  $('.datepicker').datepicker({
    format: 'mm/dd/yyyy',
    startDate: '-3d'
});
});*/

function  AjaxGetOptionSelect(){
  /*pedir mediante ajax las opciones para llenar los select de form */
  $.ajax({
    url: "AjaxGetOptionSelect",
    type: 'POST',
    data: $(formCompra).serialize(),
    success: function(response){
      console.log("response", response)
      let responseJson = response;
      
      if (responseJson.Generado){
        if(responseJson.Generado[0].produc_json){
          for (var prod of Object.values(responseJson.Generado[0].produc_json)){
            // Cargar la lista de opciones del select de productos.
            op = "<option value= '" + prod.id + "' > " + prod.text + "</option>"
            document.getElementById("cliente").innerHTML +=op                     
          }
        }
        if(responseJson.Generado[0].client_json){
          for (var cli of Object.values(responseJson.Generado[0].client_json)){
            // Cargar la lista de opciones del select de clientes.
            op = "<option value= '" + cli.id + "' > " + cli.text + "</option>"
            document.getElementById("cliente").innerHTML +=op                     
          }
        }



      }else{
        err = responseJson.error
        motrar = "Error: "+ err
        console.log("mostrar ", mostrar)
      }

    },
    error: function(error){
      console.log(error)
    }

  })
};



function addRowTable(data){
  //mostrar la lista de los productos ya incluidos en la compra
  console.log(data)
  
  for (x in data){
    id = (data[x].id);
    compra = (data[x].compra);
    codBar = (data[x].codBar);
    nombre = (data[x].productoNombre);
    paquetes = Number.parseFloat(data[x].paquetes).toFixed(2) ;
    unidades = Number.parseFloat(data[x].unidades).toFixed(2);
    valorPaquete = Number.parseFloat(data[x].valorPaquete).toFixed(2);
    descPreIva = Number.parseFloat(data[x].descuentoPreIva).toFixed(2);
    descPosIva = Number.parseFloat(data[x].descuentoPosIva).toFixed(2);
    iva = Number.parseFloat(data[x].iva).toFixed(2);
    flete = Number.parseFloat(data[x].flete).toFixed(2);
    neto = Number.parseFloat(data[x].neto).toFixed(2);    
    if ((data[x].observacion)== null){  
      obse = "";
    }
    else{
      obse = (data[x].observacion);
    }
  //  btnEditar  = "<a href='''{% url 'compras:eliminarDetalleCompra' x.id %}''' class = '' ><i class='fas fa-pen'></i>"
    btnEditar  = "<button type='button'  data-bs-toggle='modal' data-bs-target='#modal_pago'><i class='fas fa-pen' aria-hidden='true'></i></button>"
    btnEditar  = "<button type='button'  data-bs-toggle='modal' data-bs-target='#modal_pago' class = 'btn btn-primary btn-sm' style= 'width=35px;'><i class='fas fa-pen' aria-hidden='true'></i></button>"
    btnElimiar = "<a href='''{% url 'compras:eliminarDetalleCompra' x.id %}''' class = '' ><i class='fas fa-trash-alt'></i>"
  
    btns = btnEditar + "&nbsp;&nbsp;" + btnElimiar
    
    tdtd =  "</td><td>"
    tdtd_r =  "</td><td class='text-end'>"

    //TODO Mostrar datos resumen
    
    var fila="<tr><th scope='row'> " +  id + "</th><td>"+ codBar + tdtd + nombre + tdtd + paquetes  + tdtd + unidades + tdtd + valorPaquete + tdtd_r + descPreIva +  tdtd_r + iva + tdtd_r +  descPosIva + tdtd_r + flete + tdtd_r + neto + tdtd_r + obse + tdtd + btns + "</td></tr>";
    
    console.log(fila)
    let ntr = document.createElement("TR")
    ntr.innerHTML = fila
    //let tabla = document.getElementById('tb_compraDetalles')   
    document.getElementById('tb_compraDetalles').appendChild(ntr);
    //tabla.appendChild(ntr);
  }
    
}
//const ventaa = JSON.parse(document.getElementById('datoss').textContent);
//console.log(ventaa)

/*
var modalEditarVenta = document.getElementById('modal_editar_venta')
modalEditarVenta.addEventListener('show.bs.modal', function (event) {
   // Cargar los valores de la venta activa
  
  var vrventa = document.getElementById('venta')
  var vrfecha_venta = document.getElementById('fecha_venta')
  var vrcliente = document.getElementById('cliente')
  var vrfecha_vence = document.getElementById('fecha_vence')
  var vrvendedor = document.getElementById('vendedor')
  var vrpreventa = document.getElementById('preventa')
  var vrforma_pago = document.getElementById('forma_pago')
  var vrnota = document.getElementById('nota')

  console.log("venta" , vrventa.dataset.dataventa)
  console.log("fecha_venta" , vrfecha_venta.dataset.datafechaventa)
  console.log("Cliente ", vrcliente.dataset.datacliente)
  console.log("fecha_vence" , vrfecha_vence.dataset.datafechavence)
  console.log("vendedor" , vrvendedor.dataset.datavendedor)
  console.log("preventa" , vrpreventa.dataset.datapreventa)
  console.log("forma_pago" , vrforma_pago.dataset.dataformapago)
  console.log("nota", vrnota.dataset.datanota)
  
  
  document.getElementById('id_venta').value = vrventa.dataset.dataventa
  document.getElementById('id_fecha_venta').value = vrfecha_venta.dataset.datafechaventa
  document.getElementById('id_cliente').value = vrcliente.dataset.datacliente
  document.getElementById('id_fecha_vence').value = vrfecha_vence.dataset.datafechavence
  document.getElementById('id_vendedor').value = vrvendedor.dataset.datavendedor
  document.getElementById('id_preventa').value = vrpreventa.dataset.datapreventa
  document.getElementById('id_forma_pago').value = vrforma_pago.dataset.dataformapago
  document.getElementById('id_nota').value = vrnota.dataset.datanota
})
*/
/*
function ajaxValidarVenta(){
  //puedo borrarla
  var formVenta = '#formVenta';
  $.ajax({
      //url: "{% url 'ajaxValidarVenta' %}",
      url: "ajaxValidarVenta",
      type: "POST",
      data: {
        'formVenta': $(formVenta).serialize(),
        'idVenta' : document.getElementById('id_factura').value
      },
      success: function(data) {
          if (!(data['success'])) {
              // Here we replace the form, for the
              $(formVenta).replaceWith(data['venta']);
              alert("Faltan datos")
          }
          else {
              // Here you can show the user a success message or do whatever you need
              $(formVenta).find('.success-message').show();
          }
      },
      error: function () {
          $(formVenta).find('.error-message').show()
      }
  });
}

function crearVenta(){
  //puedo borrarla
  console.log("llegando a crearVenta")
  let formVenta = '#formVenta';
  console.log($(formVenta).serialize())
  $.ajax({
      //url: "{% url 'crearVenta' %}",
      url: "crearVenta",
      type: "POST",
      data: $(formVenta).serialize(),
      success: function(data) {
          console.log(data['success'])
          if (!(data['success'])) {
              // Here we replace the form, for the
              $(formVenta).replaceWith(data['venta']);
              alert("Faltan datos")
          }
          else {
              // Here you can show the user a success message or do whatever you need
              $(formVenta).find('.success-message').show();
          }
      },
      error: function () {
          $(formVenta).find('.error-message').show()
      }
  });
}
*/

