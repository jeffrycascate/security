function ClientTblSetup(table) {
}

$(document).ready(function () {
    $("#ClientTblPlaceHolder").replaceWith('<table id="ClientTbl"><caption >Supervisor</caption></table>');
    $("#ClientTbl").bootstrapTable({
        maintainSelected: true,
        pagination: true,
        pageSize: 10,
        uniqueId: 'CustomNumeric',
        sidePagination: 'client',
        search: true,
        showColumns: true,
        showExport: true,
        exportDataType: 'all',
        exportOptions: { maxNestedTables: 0 },
        exportTypes: ['json', 'xml', 'csv', 'txt', 'excel'],
        detailView: true,
        //onExpandRow: UserRelationshipManagerSupport.ClientTblExpandRow,
        columns: [{
            field: 'CustomNumeric',
            title: 'Identificador',
            formatter: 'UserRelationshipManagerSupport.CustomNumeric_FormatterMaskData',
            sortable: false,
            halign: 'center',
            align: 'right',
            visible: false
        }, {
            field: 'CustomString',
            title: 'Nombre',
            sortable: false,
            halign: 'center'
        }, {
            field: 'CustomStringEx',
            title: 'Apellido',
            sortable: false,
            halign: 'center'
        }, {
            field: 'eMailAddressDefault',
            title: 'Correo',
            sortable: false,
            halign: 'center'
        }]
    });

    $.ajax({
        type: 'GET',
        url: "https://localhost:5001/api/host",
        dataType: "json",
        data: JSON.stringify({
            filter: ''
        }),
        success: function (data) {
            if (data.d.Success === true) {
                $('#ClientTbl').bootstrapTable('load', data.d.Data !== null ? data.d.Data : []);
            }
            else
                generalSupport.NotifyFail(data.d.Reason, data.d.Code);
        },
        error: function (qXHR, textStatus, errorThrown) {
            generalSupport.ErrorHandler(qXHR, textStatus, errorThrown);
        }
    });
});