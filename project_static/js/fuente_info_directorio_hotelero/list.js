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
                {"data": "id_establecimiento", className: "text-left"},
                {"data": "nombre_de_la_unidad_economica", className: "text-left "},
                {"data": "codigo_de_la_clase_de_actividad_scian", className: "text-cente"},
                {"data": "nombre_de_clase_de_la_actividad", className: "text-left "},
                {"data": "id", className: "text-center" },
            ],
            columnDefs: [
                {
                    targets: [-1],
                    class: 'actions-container',
                    orderable: false,
                    render: function (data, type, row) {
                        var html = '<td class="text-center" style="position: relative; background-color: aqua; text-align: center; height: 100%;">';
                        html += '<div class="icon-container">';
                        html += '<i class="far fa-eye" onclick="location.href=\'{% url \'dashboard:inventario_hotelero_ent_nac_list\' %}\'"></i>';
                        html += '<i class="far fa-eye" onclick="location.href=\'{% url \'dashboard:inventario_hotelero_ent_nac_list\' %}\'"></i>';
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
            $('#dataTable tbody tr').addClass('text-left table-body mt-2');
        });
    }
};

$(function () {
    datatur.list();
});