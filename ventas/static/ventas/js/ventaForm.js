$(document).ready(function() {
  console.log( "ready!" );
  $('#modal_guardar_venta').modal('toggle'); // mostar el modal

});

//función para adicionar o restar un día a la fecha al presionar -/+
let campo_fecha = document.querySelectorAll('.dateinput');
for (var i=0; i< campo_fecha.length; i++){
  campo_fecha[i].addEventListener("keydown", function (event) {  
    let = fechaA = new Date(this.value + "T00:00:00") // agrego el texto de la hora para el ajuste al la configuracion regional local
    // ver que tecla se ha presionado
    switch(event.code) {
      case "NumpadAdd": // tecla mas del teclado alfanumérico
        var suma = fechaA.getTime() + 86400000; // milisegundos en un día 1000*60*60*24
        this.value = formatearFecha(suma)
        break;
      case "NumpadSubtract":
        var suma = fechaA.getTime() - 86400000;
        this.value = formatearFecha(suma);
        break;
    }
  });
}

/*
let fec_ven = document.getElementById('id_fecha_vence');
fec_ven.addEventListener("keydown", function (event) {
    // The parameter event is of the type KeyboardEvent
    let = fechaA = new Date(fec_ven.value + "T00:00:00") // agrego el texto de la hora para el ajuste al la configuracion regional local
    // ver que tecla se ha presionado
    switch(event.code) {
      case "NumpadAdd": // tecla mas del teclado alfanumérico
        var suma = fechaA.getTime() + 86400000; // milisegundos en un día
        fec_ven.value = formatearFecha(suma)
        break;
      case "NumpadSubtract":
        var suma = fechaA.getTime() - 86400000;
        fec_ven.value = formatearFecha(suma);
        break;
    }
});
*/
var modalVentaNueva = document.getElementById('modal_guardar_venta')
modalVentaNueva.addEventListener('show.bs.modal', function (event) {
  // Asignar valores por defecto a los compos basicos

  var ventaid = document.getElementById('ventaid');
  console.log(ventaid.dataset.ventaid)
  if (ventaid.dataset.ventaid == ""){
    var f = new Date();
    dia = `${(f.getDate())}`.padStart(2,'0');
    mes= `${(f.getMonth()+1)}`.padStart(2,'0');
    agno = f.getFullYear();  

    fecha = agno + "-" + mes + "-" + dia
    document.getElementById('id_fecha_venta').value = fecha
    document.getElementById('id_cliente').value = 1
    document.getElementById('id_valor_venta').value = 0
    document.getElementById('id_fecha_vence').value = fecha
    document.getElementById('id_vendedor').value = parseInt(document.getElementById('userName').value)
  }
})

function formatearFecha(fecha){
  var f = new Date(fecha);
  dia = `${(f.getDate())}`.padStart(2,'0');
  mes= `${(f.getMonth()+1)}`.padStart(2,'0');
  agno = f.getFullYear();  

  return agno + "-" + mes + "-" + dia
}


function cerrarModal(){
  alert("cerrarModal")
  $('#modal').modal('hide');
}
/*
$(function(){
  $('.datepicker').datepicker({
    format: 'mm/dd/yyyy',
    startDate: '-3d'
});
});*/