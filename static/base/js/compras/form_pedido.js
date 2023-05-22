var tblPedido;

// Estructura para el detalle de pedidos



var pedido = {
    items: {    
        products: []
    },
    add: function (item) {
        this.items.products.push(item);
        this.list();
    },
    list: function () {
        tblPedido = $('#tblPedido').DataTable({
            responsive: true,
            destroy: true,
            data: this.items.products,
            ordering: false,
            columns: [
                {"data": "codigo_producto"},
                {"data": "nombre"},
                {"data": "description"},
                {"data": "cantidad"},
                {"data": "id"},
            ],
            columnDefs: [
                {
                    targets: [0],
                    class: "text-center",
                    width: "10%",
                    orderable: false,
                },
                {
                    targets: [1],
                    class: "text-center",
                    width: "20%",
                    orderable: false,                
                },
                {
                    targets: [2],
                    class: "text-center",
                    width: "20%",
                    orderable: false,                
                },                
                {
                    targets: [3],
                    width: "8%",
                    class: "text-center",
                    orderable: false,  
                    render: function (data, type, row) {
                        return '<input type="text" name="cantidad" class="form-control form-control-sm input-sm" autocomplete="off" value="' + row.cantidad + '">';
                    }                 
                },
                {
                    targets: [4],
                    class: "text-center",
                    width: "5%",
                    orderable: false,
                    render: function (data, type, row) {
                        return '<a rel="remove" class="btn btn-danger m-0 p-0"><i class="fa fa-trash m-1" style="color: white" aria-hidden="true"></i>\n</i></a>'
                    }
                },
            ],
            rowCallback(row, data, displayNum, displayIndex, dataIndex) {
                $(row).find('input[name="cantidad"]').TouchSpin({
                    min: 1,
                    max: 1000000000,
                    step: 1,
                    boostat: 5,
                    maxboostedstep: 10,
                }).keypress(function (e) {
                    return validate_form_text('numbers', e, null);
                });
            },
            language: {                    
                decimal: "",
                emptyTable: "No hay información",
                info: "Mostrando _START_ a _END_ de _TOTAL_ Entradas",
                infoEmpty: "Mostrando 0 de 0 Entradas",
                infoFiltered: "(Filtrado de _MAX_ total entradas)",
                infoPostFix: "",
                thousands: ",",
                lengthMenu: "Mostrar _MENU_ Entradas",
                loadingRecords: "Cargando...",
                processing: "Procesando...",
                search: "Buscar:",
                zeroRecords: "Sin resultados encontrados",
                paginate: {
                    first: "Primero",
                    last: "Ultimo",
                    next: "Siguiente",
                    previous: "Anterior",
                },
            },
        });
    }
}

function all_delete(title, content, callback) {
    Swal.fire({
        title: title,
        text: content,
        icon: "warning",
        buttons: true,
        dangerMode: true,
    })
    .then((willDelete) => {
        if (willDelete) {
            Swal.fire("Se ha eliminado correctamente", {
                icon: "success",
            });
            callback();
            } else {
                Swal.fire("Cancelado");
            }
    });
}

$(function () {
    $('#search').on('select2:select', function (e) {
        var data = e.params.data;
        data['cantidad'] = 1;
        
        //data['subtotal'] = 0;
        //se agrega los datos a la estructura
        pedido.add(data)
        // borra luego de la seleccion
        $(this).val('').trigger('change.select2');
    });

    $('.btnRemoveAll').on('click', function () {
        if (pedido.items.products.length === 0) return false;
        all_delete('Notificación', '¿Estás seguro de eliminar todos los detalles del pedido', function () {
            pedido.items.products = [];
            pedido.list();
        });
    });

    $('#tblPedido').on('click', 'a[rel="remove"]', function () {
        var tr = tblPedido.cell($(this).closest('td, li')).index();
        pedido.items.products.splice(tr.row, 1);
        pedido.list();
    }).on('change', 'input[name="cantidad"]', function () {
        var cant = parseInt($(this).val());
        var tr = tblPedido.cell($(this).closest('td, li')).index();
        pedido.items.products[tr.row].cantidad = cant;
    });

    $('form').on('submit', function (e) {
        e.preventDefault();       
        var parameters = new FormData();
        if(pedido.items.products.length == 0){
            Swal.fire({
                title: "Notificación",
                text: "Debe cargar al menos un producto para el pedido!",
                icon: "warning",
                button: "Ok",
            })
        }else{
            parameters.append('pedido', JSON.stringify(pedido.items));
            var csrf = $('input[name="csrfmiddlewaretoken"]').val();
            parameters.append('csrfmiddlewaretoken', csrf);
            submit_with_ajax(window.location.pathname, 'Notificación', '¿Desea registrar este pedido?', parameters, function () {
                location.href = "/compra/listPedidosCompra/"
            });
        }        
    });
});

// validar entrada
function validate_form_text(type, event, regex) {
    var key = event.keyCode || event.which;
    var numbers = (key > 47 && key < 58) || key === 8;
    var numbers_spaceless = (key > 47 && key < 58);
    var letters = !((key !== 32) && (key < 65) || (key > 90) && (key < 97) || (key > 122 && key !== 241 && key !== 209 && key !== 225 && key !== 233 && key !== 237 && key !== 243 && key !== 250 && key !== 193 && key !== 201 && key !== 205 && key !== 211 && key !== 218)) || key === 8;
    var letters_spaceless = !((key < 65) || (key > 90) && (key < 97) || (key > 122 && key !== 241 && key !== 209 && key !== 225 && key !== 233 && key !== 237 && key !== 243 && key !== 250 && key !== 193 && key !== 201 && key !== 205 && key !== 211 && key !== 218)) || key === 8;
    var decimals = ((key > 47 && key < 58) || key === 8 || key === 46);

    if (type === 'numbers') {
        return numbers;
    } else if (type === 'letters') {
        return letters;
    } else if (type === 'numbers_letters') {
        return numbers || letters;
    } else if (type === 'letters_spaceless') {
        return letters_spaceless;
    } else if (type === 'letters_numbers_spaceless') {
        return letters_spaceless || numbers_spaceless;
    } else if (type === 'decimals') {
        return decimals;
    } else if (type === 'regex') {
        return regex;
    }
    return true;
}
