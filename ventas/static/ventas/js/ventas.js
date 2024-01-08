$(document).ready(function() {
  console.log( "ready!" );
  $(document.getElementsByName('observacion')).attr('rows', '1');       
  //$('#modal_nueva_venta').modal('toggle'); // mostar el modal
});

$('#tabla_items').DataTable({
  "responsive": true,
  language: {  
    url: '//cdn.datatables.net/plug-ins/1.13.6/i18n/es-CO.json',
  },
  }  
);

function nuevaVenta(){
  //// Asignar valores por defecto a los compos basicos
  // puedo borrarlo
  var f = new Date();
  dia = `${(f.getDate())}`.padStart(2,'0');
  mes= `${(f.getMonth()+1)}`.padStart(2,'0');
  agno = f.getFullYear();

  fecha = agno + "-" + mes + "-" + dia
  document.getElementById('id_fecha_venta').value = fecha
  document.getElementById('id_cliente').value = 1
  document.getElementById('id_valor_venta').value = 0
  document.getElementById('id_fecha_vence').value = fecha
  document.getElementById('id_fecha_vence').value = fecha

}

var modal_nueva_venta = document.getElementById('modal_nueva_venta')
modal_nueva_venta.addEventListener('show.bs.modal', function (event) {
  // Asignar valores por defecto a los compos basicos

  document.getElementById('id_fecha_venta').value = fechaActual()
  document.getElementById('id_cliente').value = 1
  document.getElementById('id_valor_venta').value = 0
  document.getElementById('id_fecha_vence').value = fechaActual()
  document.getElementById('id_vendedor').value = parseInt(document.getElementById('userName').value)

})

// function ajaxValidarVenta(){
//   //puedo borrarla
//   var formVenta = '#formVenta';
//   $.ajax({
//       //url: "{% url 'ajaxValidarVenta' %}",
//       url: "ajaxValidarVenta",
//       type: "POST",
//       data: {
//         'formVenta': $(formVenta).serialize(),
//         'idVenta' : document.getElementById('id_factura').value
//       },
//       success: function(data) {
//           if (!(data['success'])) {
//               // Here we replace the form, for the
//               $(formVenta).replaceWith(data['venta']);
//               alert("Faltan datos")
//           }
//           else {
//               // Here you can show the user a success message or do whatever you need
//               $(formVenta).find('.success-message').show();
//           }
//       },
//       error: function () {
//           $(formVenta).find('.error-message').show()
//       }
//   });
// }

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


function ajaxValidarVentaDetalle(){
  let formVentaDetalle = '#formVentaDetalle';
  console.log("ajaxValidarVentaDetalle")
  
  // asignar a cada item el número de la factura activa.
  document.getElementById('id_venta').value = document.getElementById('id_factura').value

  var venta = document.getElementById('id_venta').value;        
  var producto = document.getElementById('id_producto').value;        
  var cantidad = document.getElementById("id_cantidad").value;
  var valor_unitario = document.getElementById("id_valor_unitario").value;  
  var descuento = document.getElementById("id_descuento").value;
  var observacion = document.getElementById("id_observacion").value;

  console.log(producto, " ", cantidad, " ", valor_unitario, " ", descuento, " ", observacion, " -- ", venta )
  console.log($(formVentaDetalle).serialize())
  
  $.ajax({
      url: "ajaxValidarVentaDetalle",
      type: "POST",
      data: $(formVentaDetalle).serialize(),
      success: function(data) {
          if (data['success']) {
              // Here we replace the form, for the
              console.log("success")
              console.log(producto, " ", cantidad, " ", valor_unitario, " ", descuento, " ", observacion)

              var tabla = $("#tabla_items").dataTable();
              tabla.fnAddData([
              //  tabla.row.add([
                data['idDetalle'],
                producto, 
                cantidad, 
                valor_unitario, 
                descuento, 
                observacion, 
                '<div class="td action"><button type="button" onclick="edit(this);">edit</button></div>'
              ])

              
              let TB_dvyr = $("#tb_detalles_venta_ya_registrados").append("<tr></tr>");
              TB_dvyr.append("<td>"+ producto + "</td>")
              TB_dvyr.append("<td>"+ cantidad + "</td>")
              TB_dvyr.append("<td>"+ valor_unitario + "</td>")
              TB_dvyr.append("<td>"+ descuento + "</td>")
              TB_dvyr.append("<td>"+ observacion + "</td>")

              var contendor  = $("#tb_detalles_venta_ya_registrados").html();
              var nuevaFila   = '<tr>';
              nuevaFila   = '<td>' + producto + '</td>';
              nuevaFila  += '<td>' + cantidad + '</td>';
              nuevaFila  += '<td>' + valor_unitario + '</td>';
              nuevaFila  += '<td>' + descuento + '</td>';
              nuevaFila  += '<td>' + observacion + '</td>';
              nuevaFila   = '</tr>';
              
              $("#tb_detalles_venta_ya_registrados").html(contendor+nuevaFila);

              html= '<td></td><td></td><td></td><td></td>'

            //         document.getElementById('detalles_venta_ya_registrados').insertRow(-1).innerHTML = nuevaFila

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

function addRowDT(data){
  console.log("llegando a AddRowDT")
  console.log(data)
  tabla = $("#detalles_venta_ya_registrados").dataTable();
  for(let i=0; i<data.length; i++){
      if (data[i].producto != null){
          tabla.fnAddData([                
              data[i].producto,
              data[i].cantidad,
              data[i].valor_unitario,
              data[i].descuento,
              data[i].observacion,             
              /*
              '<Button value="actualizar" title="Actualizar" class="btnEditar" data-targe="#miModal" data-toggle="modal">Digitalizar</button> &nbsp;'*/
          ])
      }
  }
}

// $('#modal_nueva_venta1).modal('toggle')  mostar el modal        
