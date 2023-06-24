$.datepicker.regional['es'] = {
    closeText: 'Cerrar',
    prevText: '< Ant',
    nextText: 'Sig >',
    currentText: 'Hoy',
    monthNames: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'],
    monthNamesShort: ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'],
    dayNames: ['Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado'],
    dayNamesShort: ['Dom', 'Lun', 'Mar', 'Mié', 'Juv', 'Vie', 'Sáb'],
    dayNamesMin: ['Do', 'Lu', 'Ma', 'Mi', 'Ju', 'Vi', 'Sá'],
    weekHeader: 'Sm',
    dateFormat: 'dd/mm/yy',
    firstDay: 1,
    isRTL: false,
    showMonthAfterYear: false,
    yearSuffix: ''
};
$.datepicker.setDefaults($.datepicker.regional['es']);

$('[data-toggle="tooltip"]').tooltip()

function abrir_modal_edicion(url) {
	$('#edicion').load(url, function () {
		$(this).modal('show');
	});
}
function abrir_modal_creacion(url) {
	$('#creacion').load(url, function () {
		$(this).modal('show');
	});
}
function abrir_modal_eliminacion(url) {
	$('#eliminacion').load(url, function () {
		$(this).modal('show');
	});
}
function cerrar_modal_creacion(){
	$('#creacion').modal('hide');
}

function cerrar_modal_edicion() {
	$('#edicion').modal('hide');
}
function cerrar_modal_eliminacion() {
	$('#eliminacion').modal('hide');
}

function aceptarLetras(e) {
	e.value = e.value.replace(/[^A-Za-zÀ-ÿ\u00f1\u00d1\s-]+$/g, '')
}

function aceptarNumeros(e) {
	e.value = e.value.replace(/[^0-9-]/g, '')
}

function aceptarNumerosYLetras(e) {
	e.value = e.value.replace(/[^A-Za-zÀ-ÿ0-9\u00f1\u00d1\s-/g]+$/g, '')
}

function validateSpaceBlank(e){
	if (e.value.trim().length == 0)
		e.value = ""
}

// Función para eliminar los registros de forma genérica
// con el sweet alert
function eliminar_registro(url, redirect_url) { 
	Swal.fire({
		"title":"¿Estás seguro que quiere eliminar?",
		"text":"Esta acción no se puede deshacer.",
		"icon":"question",
		"showCancelButton":true,
		"cancelButtonText":"No, Cancelar",
		"confirmButtonText":"Si, Eliminar",
		"reverseButtons":true,
		"confirmButtonColor":"#dc3545",
		"showLoaderOnConfirm": true,
		"preConfirm": function(login)  {
			return $.get(url,function(result) {
				return result;
			})
			.fail(function(error) {
				Swal.fire({
					title:'Error',
					text:'Ha Ocurrido un error, intente mas tarde',
					icon:'error',
					confirmButtonColor: '#007bff',
				});
			})
		}
	})
	.then(function(result) {
		if(result.value) {
			if (result.value.error) {
				Swal.fire({
					title:'Error',
					text:result.value.message,
					icon:'error',
					confirmButtonColor: '#007bff',
				});
			}else{
				Swal.fire({
					title: 'Éxito',
					text: result.value.message,
					icon: 'success',
					confirmButtonColor: '#007bff',
					showCancelButton: false,
					allowOutsideClick: false
				}).then(function(result)  {
					window.location.href = redirect_url;
				});

			}
		}
	});
}

function add_edit_registro(text) { 
	Swal.fire({
		title: 'Éxito',
		text: text,
		icon: 'success',
		confirmButtonColor: '#007bff',
		showCancelButton: false,
		allowOutsideClick: false
	});
}

function warning_registro(text) { 
	Swal.fire({
		title: 'Notificación',
		text: text,
		icon: 'warning',
		confirmButtonColor: '#007bff',
	});
}


function submit_with_ajax(url, title, content, parameters, callback) {
    Swal.fire({
        title: title,
        text: content,
        icon: "warning",
        buttons: true,
        dangerMode: true,
    })
    .then((confir) => {
        if(confir){
            $.ajax({
                url: url,
                type: 'POST',
                data: parameters,
                dataType: 'json',
                processData: false,
                contentType: false,
                success: function (response) {
                    if(response.mensaje != "error"){
                        Swal.fire({
                            title: 'Notificación',
                            text: 'Se ha Registrado Correctamente',
                            icon: 'success',
							confirmButtonColor: '#007bff',
                        });
                        callback();
                    }
                    else
                    {
                        Swal.fire({
                            title: 'Notificación',
                            text: 'ha ocurrido un error, intenlo de nuevo',
                            icon: 'error',
							confirmButtonColor: '#007bff',
                        });
                    }                                     
                },
                error: function (xhr, ajaxOptions, thrownError) {
                    swal("Error", xhr + ' ' + ajaxOptions + ' ' + thrownError, "error");
                }
            });
        }
        else{
            Swal.fire("Cancelado");
        }
        
    });
}

function add_miles(value){
    return value.toString().replace(/\D/g, "")
                        .replace(/([0-9])([0-9]{3})$/, '$1.$2')
                        .replace(/\B(?=(\d{3})+(?!\d)\.?)/g, ".");
}

function anular_factura (url, redirect_url) { 
	Swal.fire({
		"title":"¿Estás seguro que quiere anular la factura?",
		"text":"Esta acción no se puede deshacer.",
		"icon":"question",
		"showCancelButton":true,
		"cancelButtonText":"No, Cancelar",
		"confirmButtonText":"Si, Eliminar",
		"reverseButtons":true,
		"confirmButtonColor":"#dc3545",
		"showLoaderOnConfirm": true,
		"preConfirm": function(login)  {
			return $.get(url,function(result) {
				return result;
			})
			.fail(function(error) {
				Swal.fire({
					title:'Error',
					text:'Ha Ocurrido un error, intente mas tarde',
					icon:'error',
					confirmButtonColor: '#007bff',
				});
			})
		}
	})
	.then(function(result) {
		if(result.value) {
			if (result.value.error) {
				Swal.fire({
					title:'Error',
					text:result.value.message,
					icon:'error',
					confirmButtonColor: '#007bff',
				});
			}else{
				Swal.fire({
					title: 'Éxito',
					text: result.value.message,
					icon: 'success',
					confirmButtonColor: '#007bff',
					showCancelButton: false,
					allowOutsideClick: false
				}).then(function(result)  {
					window.location.href = redirect_url;
				});

			}
		}
	});
}

function return_colors(){
	var colors = [];
	while (colors.length < 100) {
		do {
			var color = Math.floor((Math.random()*1000000)+1);
		} while (colors.indexOf(color) >= 0);
		colors.push("#" + ("000000" + color.toString(16)).slice(-6));
	}
	return colors;
}


var compareDate = function(fecha_emision, fecha_vencimiento){
	var d1 = fecha_emision.split("/");
	var d2 = fecha_vencimiento.split("/");
	var c = new Date();

	var from = new Date(d1[2], parseInt(d1[1])-1, d1[0]);  // -1 because months are from 0 to 11
	var to   = new Date(d2[2], parseInt(d2[1])-1, d2[0]);
	var check = new Date(c.getFullYear(), c.getMonth(), c.getDate());
	if(check >= from && check <= to){
		return true
	}
	return false
}

var compareDateReporte = function(fecha_emision, fecha_vencimiento){
	var d1 = fecha_emision.split("/");
	var d2 = fecha_vencimiento.split("/");

	var from = new Date(d1[2], parseInt(d1[1])-1, d1[0]);  // -1 because months are from 0 to 11
	var to   = new Date(d2[2], parseInt(d2[1])-1, d2[0]);

	if(from <= to){
		return true
	}
	return false
}