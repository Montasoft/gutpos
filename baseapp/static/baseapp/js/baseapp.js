$(document).ready(function() {
    console.log("ready!");

});




(function($) {

	"use strict";

	var fullHeight = function() {

		$('.js-fullheight').css('height', $(window).height());
		$(window).resize(function(){
			$('.js-fullheight').css('height', $(window).height());
		});

	};
	fullHeight();

	$('#sidebarCollapse').on('click', function () {
      $('#sidebar').toggleClass('active');
  });

})(jQuery);

function abrirModal(modal, url){
  console.log(url)
  console.log('#'+ modal)
  //$('#modal_pago').modal('show');
  var url_ = "{% url '" + url + "' %}"
  console.log(url_)
  $('#'+ modal).load(url, function(){
    $(this).modal('show');
  });
}

function fechaActual(){
  var f = new Date();
  dia = `${(f.getDate())}`.padStart(2,'0');
  mes= `${(f.getMonth()+1)}`.padStart(2,'0');
  agno = f.getFullYear();

  fecha = agno + "-" + mes + "-" + dia
  return fecha
}



function formatoMoneda(numero, decimales){
  const formateando = new Intl.NumberFormat('es-US',{
    style: 'currency',
    minimumFractionDigits: decimales,
    currency: 'USD'
  });
  return formateando.format(numero)
}