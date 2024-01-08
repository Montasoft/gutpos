
$(document).ready(function() {
  console.log("ready!");
  $(document.getElementsByName('observacion')).attr('rows', '1');               
  document.getElementById('final').scrollIntoView(true)
  scrollTabla()

  cargarDatosALocalStorage() // carga la lista de productos


  $("#id_observacion").blur(function(){
    document.getElementById("btnAdd").focus(); //pasar el foco a btnAdd
});


  $('#tabla_items').DataTable({
    'pageLength': -1,
    "searching": true,
    "responsive": true,
    "bLengthChange" : false, //thought this line could hide the LengthMenu  
    //"bInfo":false,   
    language: {
      "decimal": "",
      "emptyTable": "No hay información",
      "info": "Mostrando _START_ a _END_ de _TOTAL_ Entradas",
      "infoEmpty": "Mostrando 0 to 0 of 0 Entradas",
      "infoFiltered": "(Filtrado de _MAX_ total entradas)",
      "infoPostFix": "",
      "thousands": ",",
      "lengthMenu": "Mostrar _MENU_ Entradas",
      "loadingRecords": "Cargando...",
      "processing": "Procesando...",
      "search": "Buscar:",
      "zeroRecords": "Sin resultados encontrados",
      "paginate": {
          "first": "Primero",
          "last": "Ultimo",
          "next": "Siguiente",
          "previous": "Anterior"
      }
    } 
  });
  
});


function cargarDatosALocalStorage(){

    //cargar lista de productos al local storage
    var jsonProductos = JSON.parse(document.getElementById('productos').textContent)
//    console.log("productos" , jsonProductos)

    for (let producto of jsonProductos){
      localStorage.setItem(producto.id, JSON.stringify(producto));  
    }
    
    for(let i=0; i<localStorage.length; i++) {
      let key = localStorage.key(i);
//      console.log(`${key}: ${localStorage.getItem(key)}`);
      let thisproduc =JSON.parse(localStorage.getItem(key))
  //    console.log(thisproduc.nombre)
    }
}

function leerLocalStorage(){
  //para traer a pantalla los datos de nombre y precio al ingresar codigo valido
  console.log("recibo: ",   )
  var codIngresado = document.getElementById("codIngresado").value;
  console.log("codIngresado: ", codIngresado);
  prod = JSON.parse(localStorage.getItem(codIngresado));

  console.log(prod.nombre);
  console.log(prod.precioVenta);
  

  document.getElementById("id_producto").value = prod.id;
  document.getElementById("id_cantidad").value = 1;
  document.getElementById("id_valor_unitario").value = prod.precioVenta;
  document.getElementById("btnAdd").focus();

}


function ajaxValidarVentaDetalle(){
  let formVentaDetalle = '#formVentaDetalle';
  let total = document.getElementById('totalVenta')
  console.log("ajaxValidarVentaDetalle")
  
  // asignar el número de la venta activa.
  document.getElementById('id_venta').value = document.getElementById('venta').value

  console.log($(formVentaDetalle).serialize())
  
  var url_post = $("#formVentaDetalle").data("post-url");
  $.ajax({
      url: url_post,
      type: "POST",
      data: $(formVentaDetalle).serialize(),
      success: function(data) {
          if (data['success']) {
              // proceso retorna con exito
              console.log("success")            
              
              //tomo los datos para mostrarlo en la tabla
              let datos = []
              datos.push(data['detalleCreado'])
              addRowTable(datos)

              total.value =(data['detalleCreado'].total_venta)

              //desplazo el scroll para mostra el ultimo registro
              scrollTabla()
              document.getElementById('formVentaDetalle').reset()
              document.getElementById('codIngresado').focus() 
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

function scrollTabla(){
  var tabla = document.getElementById('tVentaDetalles');
  // TODO Medir el scroll y dar la medida excacta
  tabla.scrollTop = '9999'; 
}

function abrirModal(url, Idmodal){
  console.log(url)
  //$('#modal_pago').modal('show');
  var url_ = "{% url '" + url + "' %}"
  console.log(url_)
  $('#'+ Idmodal).load(url, function(){
    $(this).modal('show');
  });
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
    data: $(formVenta).serialize(),
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
  //mostrar la lista de los productos ya incluidos en la venta
  console.log(data)
  
  for (x in data){
    id = (data[x].id);
    prod = (data[x].producto);
    nomb = (data[x].nombre);
    cant = Number.parseFloat(data[x].cantidad).toFixed(2) ;
    valu = Number.parseFloat(data[x].valor_unitario).toFixed(2);
    desc = Number.parseFloat(data[x].descuento).toFixed(2);
    iva = Number.parseFloat(data[x].iva).toFixed(2);
    neto = Number.parseFloat(data[x].neto).toFixed(2);    
    if ((data[x].observacion)== null){
      obse = "";
    }
    else{
      obse = (data[x].observacion);
    }
    

    btnEditar  = "<a href='''{% url 'POS:eliminarDetalleVenta' x.id %}''' class = '' ><i class='fas fa-pen'></i>"
    btnElimiar = "<a href='''{% url 'POS:eliminarDetalleVenta' x.id %}''' class = '' ><i class='fas fa-trash-alt'></i>"
  
    btns = btnEditar + "&nbsp;&nbsp;" + btnElimiar
    
    tdtd =  "</td><td>"
    tdtd_r =  "</td><td class='text-end'>"
     
    var fila="<tr><th scope='row'> " +  id + "</th><td>"+ prod + tdtd + nomb + tdtd_r + cant + tdtd_r + valu + tdtd_r + desc + tdtd_r + iva + tdtd_r + neto + tdtd +   obse + tdtd + btns + "</td></tr>";
    
    console.log(fila)
    let ntr = document.createElement("TR")
    ntr.innerHTML = fila
    //let tabla = document.getElementById('tb_ventaDetalles')   
    document.getElementById('tb_ventaDetalles').appendChild(ntr);
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

