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
        console.log("Ejecutando proyectos_inv", window.location.pathname); // Mensaje de depuració
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
                {"data": "id_del_proyecto", className: "text-left tb-text "},
                {"data": "destino", className: "text-left tb-text "},
                {"data": "nombre_del_proyecto", className: "text-left tb-text "},
                {"data": "giro", className: "text-left tb-text "},
                {"data": "estatus", className: "text-left tb-text "},
                {"data": "monto_comprometido_del_proyecto_mxn", className: "text-left tb-text "},
                {"data": "id_del_proyecto", className: "text-left  actions-column tb-text"},
            ],columnDefs: [
                {
                    targets: [-1],
                    class: 'actions-container',
                    orderable: false,
                    render: function (data, type, row) {
                        var html = '<td class="text-center" style="position: relative; text-align: center; height: 100%;">';
                        html += '<div class="icon-container">';
                        html += '<i class="fas fa-edit" onclick="location.href=\'edit/' + row.id_del_proyecto + '/\'"></i>';
                        html += '<form method="post" action="delete/' + row.id_del_proyecto + '/">';
                        html += '<input type="hidden" name="csrfmiddlewaretoken" value="' + csrftoken + '">';
                        html += '<button type="submit" class="ml-1 mr-1 actions-btn delete-r" id="delete-r">';
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