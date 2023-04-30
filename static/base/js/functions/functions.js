/*
* Tira una alerta de eliminacion tiene
* callback es la funcion que recibe para luego de la acción
* */
function alert_delete(title, content, callback) {
    swal({
        title: title,
        text: content,
        icon: "warning",
        buttons: true,
        dangerMode: true,
    })
    .then((willDelete) => {
        if (willDelete) {
            swal("Se ha eliminado correctamente", {
                icon: "success",
            });
            callback();
            } else {
                swal("Cancelado");
            }
    });
}

/*
*Para enviar datos del formulario con ajax
* */
function submit_with_ajax(url, title, content, parameters, callback) {
    swal({
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
                        swal({
                            title: 'Notificación',
                            text: 'Se ha Registrado Correctamente',
                            icon: 'success'
                        });
                        callback();
                    }
                    else
                    {
                        swal({
                            title: 'Notificación',
                            text: 'ha ocurrido un error, intenlo de nuevo',
                            icon: 'error'
                        });
                    }                                     
                },
                error: function (xhr, ajaxOptions, thrownError) {
                    swal("Error", xhr + ' ' + ajaxOptions + ' ' + thrownError, "error");
                }
            });
        }
        else{
            swal("Cancelado");
        }
        
    });
}


function validate_ajax(url, title, content, parameters, callback) {
    swal({
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
                        swal({
                            title: 'Notificación',
                            text: 'Se ha Registrado Correctamente',
                            icon: 'success'
                        });
                        callback();
                    }
                    else
                    {
                        swal({
                            title: 'Notificación',
                            text: 'ha ocurrido un error, intenlo de nuevo',
                            icon: 'error'
                        });
                    }                                     
                },
                error: function (xhr, ajaxOptions, thrownError) {
                    swal("Error", xhr + ' ' + ajaxOptions + ' ' + thrownError, "error");
                }
            });
        }
        else{
            swal("Cancelado");
        }
        
    });
}