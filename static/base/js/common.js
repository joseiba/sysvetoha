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
					console.log(result);
					window.location.href = redirect_url;
				});

			}
		}
	});
}