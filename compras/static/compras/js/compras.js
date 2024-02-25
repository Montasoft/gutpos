$(document).ready(function() {
    console.log("ready! in compras.js");
});
// TRADUCIR EL MARCO DE LA DATATABLE
$('#tabla_items').DataTable({
  "responsive": true,
  language: {
    url: '//cdn.datatables.net/plug-ins/1.13.6/i18n/es-CO.json',
  },
}
);

var modal_nueva_compra = document.getElementById('modal_nueva_compra')
modal_nueva_compra.addEventListener('show.bs.modal', function (event) {
  // Asignar valores por defecto a los compos basicos
  
  console.log(fechaActual())

  document.getElementById('id_proveedor').value = 1
  document.getElementById('id_fecha_compra').value = fechaActual()
  document.getElementById('id_valor_compra').value = 0
  document.getElementById('id_forma_pago').value = 1
  document.getElementById('id_fecha_vence').value = fechaActual()
  document.getElementById('id_fecha_recibido').value = fechaActual()
  
})
