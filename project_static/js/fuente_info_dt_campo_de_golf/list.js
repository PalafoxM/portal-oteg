var csrftoken = getCookie('csrftoken');

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var datatur = {
    list: function () {
        console.log("Ejecutando datatur.list()", window.location.pathname); // Mensaje de depuració
        $('#dataTable').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            deferRender: true,
            ajax: {
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'action': 'search'
                },
                dataSrc: "",
                headers: {
                    'X-CSRFToken': csrftoken
                }
            },
            columns: [
                {"data": "id", className: "text-left pl-3"},
                {"data": "giro", className: "text-center hidden-t"},
                {"data": "clave_del_giro", className: "text-center hidden-t"},
                {"data": "nombre_comercial", className: "text-center hidden-t"},
                {"data": "rfc", className: "text-center hidden-t"},
                {"data": "id", className: "actions-container"},
            ],
            columnDefs: [
                {
                    targets: [-1],
                    class: 'actions-container',
                    orderable: false,
                    render: function (data, type, row) {
                        var buttons = '<button class="ml-1 mr-1 actions-btn" tooltip="Consultar" flow="down" onclick="location.href=\'dt-campo-golf/edit/' + row.id + '/\'">';
                        buttons += '<i class="fas fa-edit"></i>';
                        buttons += '</button> ';
                        buttons += '<form method="post" action="dt-campo-golf/delete/' + row.id + '/">';
                        buttons += '<input type="hidden" name="csrfmiddlewaretoken" value="' + csrftoken + '">';
                        buttons += '<button class="ml-1 mr-1 actions-btn" tooltip="Consultar" flow="down" onclick="return confirm(\'¿Está seguro de que desea eliminar la informacion?\');">';
                        buttons += '<i class="fas fa-trash"></i>';
                        buttons += '</button>';
                        buttons += '</form>';
                        return buttons;
                    }
                },
            ],
            initComplete: function (settings, json) {
                
            }
        });
        // Agregar clase a los elementos <tr>
        $('#dataTable').on('draw.dt', function () {
            $('#dataTable tbody tr').addClass('text-center table-body mt-2');
        });
    }
};

$(function () {
    datatur.list();
});