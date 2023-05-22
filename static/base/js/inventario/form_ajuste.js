var tblAjuste;

// Estructura para el detalle de facturas
var ajuste = {
    items: {
        products: []
    },
    calc_invoice: function () {
        var subtotal = 0
        $.each(this.items.products, function (pos, dict) {
            dict.subtotal = dict.cantidad - dict.stock_sistema;
            subtotal += dict.subtotal;
        })
    },
    add: function (item) {
        this.items.products.push(item);
        this.list();
    },
    list: function () {
        this.calc_invoice()
        tblAjuste = $('#tblAjuste').DataTable({
            responsive: true,
            destroy: true,
            data: this.items.products,
            ordering: false,
            columns: [
                {"data": "codigo_producto"},
                {"data": "nombre"},
                {"data": "description"},
                {"data": "stock_sistema"},
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
                    class: "",
                    width: "20%",
                    orderable: false,                
                },
                {
                    targets: [2],
                    class: "",
                    width: "20%",
                    orderable: false,                
                },
                {
                    targets: [3],
                    class: "text-center my-0 ",
                    width: "15%",
                    orderable: false,
                },
                {
                    targets: [4],
                    width: "15%",
                    class: "text-center",
                    orderable: false,  
                    render: function (data, type, row) {
                        return '<input type="text" name="cantidad" class="form-control form-control-sm input-sm" autocomplete="off" value="' + row.cantidad + '">';
                    }            
                },
                {
                    targets: [5],
                    class: "text-center my-0 ",
                    width: "15%",
                    orderable: false,
                },
                {
                    targets: [6],
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
                    min: 0,
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
                infoEmpty: "Mostrando 0 to 0 de 0 Entradas",
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

$(function () {
    $('#search').on('select2:select', function (e) {
        var data = e.params.data;

        data['cantidad'] = 1
                //se agrega los datos a la estructura
        ajuste.add(data)
        // borra luego de la seleccion
        $(this).val('').trigger('change.select2');
    });

    $('.btnRemoveAll').on('click', function () {
        if (ajuste.items.products.length === 0) return false;
        alert_delete('Notificación', '¿Estás seguro de eliminar todos los detalles del ajuste', function () {
            ajuste.items.products = [];
            ajuste.list();
        });
    });

    $('#tblAjuste').on('click', 'a[rel="remove"]', function () {
        var tr = tblAjuste.cell($(this).closest('td, li')).index();
        ajuste.items.products.splice(tr.row, 1);
        ajuste.list();
    }).on('keyup change', 'input[name="cantidad"]', function () {
        var cant = parseInt($(this).val());
        var tr = tblAjuste.cell($(this).closest('td, li')).index();
        ajuste.items.products[tr.row].cantidad = cant;
        ajuste.calc_invoice();
        // el 5 es el lugar donde tiene que estar el subtotal
        $('td:eq(5)', tblAjuste.row(tr.row).node()).html(ajuste.items.products[tr.row].subtotal);
    })

    $('form').on('submit', function (e) {
        if(ajuste.items.products.length == 0){
            swal({
                title: "Notificación",
                text: "Debe cargar al menos un producto para el ajuste!",
                icon: "warning",
                button: "Ok",
            })
            e.preventDefault();
        }else{
            e.preventDefault();
            var parameters = new FormData();
            parameters.append('ajuste', JSON.stringify(ajuste.items));
            var csrf = $('input[name="csrfmiddlewaretoken"]').val();
            parameters.append('csrfmiddlewaretoken', csrf);
            submit_with_ajax(window.location.pathname, 'Notificación', '¿Desea registrar este ajuste de inventario?', parameters, function () {
                location.href = "/producto/addAjusteInventario/"
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

function add_miles(value){
    return value.toString().replace(/\D/g, "")
                        .replace(/([0-9])([0-9]{3})$/, '$1.$2')
                        .replace(/\B(?=(\d{3})+(?!\d)\.?)/g, ".");
}

