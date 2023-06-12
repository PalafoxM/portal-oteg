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
                {"data": "id", className: "text-left"},
                {"data": "giro", className: "text-left tb-text "},
                {"data": "clave_del_giro", className: "text-left tb-text "},
                {"data": "nombre_comercial", className: "text-left tb-text "},
                {"data": "rfc", className: "text-left tb-text "},
                {"data": "id", className: "text-left  actions-column tb-text"},
            ],
            columnDefs: [
                {
                    targets: [-1],
                    class: 'actions-column',
                    orderable: false,
                    render: function (data, type, row) {
                        var html = '<td class="text-center" style="position: relative; background-color: aqua; text-align: center; height: 100%;">';
                        html += '<div class="icon-container">';
                        html += '<i class="fas fa-edit" onclick="location.href=\'dt-operadores/edit/' + row.id + '/\'"></i>';
                        html += '<form method="post" action="dt-operadores/delete/' + row.id + '/">';
                        html += '<input type="hidden" name="csrfmiddlewaretoken" value="' + csrftoken + '">';
                        html += '<button class="ml-1 mr-1 actions-btn" tooltip="Consultar" flow="down" onclick="return confirm(\'¿Está seguro de que desea eliminar la informacion?\');">';
                        html += '<i class="fas fa-trash"></i>';
                        html += '</button>';
                        html += '</form>';
                        html += '</div>';
                        html += '</td>';
                        // Append your existing buttons or elements here
                        return html;
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