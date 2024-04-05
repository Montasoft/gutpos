$(document).ready(function(){
    console.log("llegando a objectsview")
    var jsondatos = JSON.parse(document.getElementById('serialized_data').textContent)
    console.log (jsondatos)
    
    console.log("antes de llamar a convertirdatostabla")

// Obtener una referencia al elemento HTML donde deseas agregar la tabla
var contenedorTabla = document.getElementById('contenedor-tabla');

// Convertir el diccionario en una tabla HTML
var tablaHTML = convertirADatosTabla(jsondatos);

// Agregar la tabla al contenedor
contenedorTabla.appendChild(tablaHTML);
    //let lista = document.getElementById('campos').textContent


})


// Función para convertir un diccionario con varios registros en una tabla HTML
function convertirADatosTabla(datos) {
    console.log("dentro de convertirdatostabal")
    var tabla = document.createElement('table');
    tabla.border = '1';

    var cabecera = tabla.createTHead();
    var filaCabecera = cabecera.insertRow();

    for (var clave in datos[0]) {
        var celdaCabecera = filaCabecera.insertCell();
        celdaCabecera.textContent = clave;
    }

    var cuerpo = tabla.createTBody();

    datos.forEach(function(registro) {
        var fila = cuerpo.insertRow();
        for (var clave in registro) {
            var celda = fila.insertCell();
            celda.textContent = registro[clave];
        }
    });

    return tabla;
}



