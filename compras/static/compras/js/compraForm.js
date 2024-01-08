$(document).ready(function() {
  console.log( "ready!" );
  $('#modal_guardar_compra').modal('toggle'); // mostar el modal

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
var modalCompraNueva = document.getElementById('modal_guardar_compra')
modalCompraNueva.addEventListener('show.bs.modal', function (event) {
  // Asignar valores por defecto a los compos basicos

  var compraid = document.getElementById('compraid');
  console.log(compraid.dataset.compraid)
  if (compraid.dataset.compraid == ""){
    var f = new Date();
    dia = `${(f.getDate())}`.padStart(2,'0');
    mes= `${(f.getMonth()+1)}`.padStart(2,'0');
    agno = f.getFullYear();  

    fecha = agno + "-" + mes + "-" + dia
    document.getElementById('id_fecha_compra').value = fecha
    document.getElementById('id_fecha_vence').value = fecha
    document.getElementById('id_fecha_recibido').value = fecha
    document.getElementById('id_proveedor').value = 1
    document.getElementById('id_valor_compra').value = 0
    document.getElementById('id_fecha_vence').value = fecha
   // document.getElementById('id_vendedor').value = parseInt(document.getElementById('userName').value)
  }
})

function formatearFecha(fecha){
  var f = new Date(fecha);
  dia = `${(f.getDate())}`.padStart(2,'0');
  mes= `${(f.getMonth()+1)}`.padStart(2,'0');
  agno = f.getFullYear();  

  return agno + "-" + mes + "-" + dia
}

function abrirModal(url){
  $('#modal').modal('show');
  console.log("abrir modal")
  console.log(url)
  var url_ = "{% url '" + url + "' %}"
  console.log(url_)
 // $('#modal').load(url_, function(){
  //  $(this).modal('show');
  //});
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