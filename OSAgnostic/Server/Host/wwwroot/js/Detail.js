var DetailSupport = new function () {

    this.SuccessfullyFormatter = function (value, row, index) {
        var valueState = 'green';
        if (value === false) {
            valueState = 'red';
        }
        return '<i class="fas fa-check-circle ' + valueState + '"></i>'; 
    };


    this.SeverityFormatter = function (value, row, index) {
        var htmlValue = 'green';
        if (value === 'Warning') {
            htmlValue = '<i class="fas fa-exclamation-triangle"></i>';
        }
        if (value === 'Critical') {
            htmlValue = '<i class="fas fa-radiation-alt"></i>';
        }
        return htmlValue;
    };

    this.JobTblExpandRow = function (index, row, $detail) {
        var tblparentid = $detail.parent().parent().parent()[0].id;
        var html = [];

        html.push('<table id="grid5Tbl-' + row.Id + '" data-tblparentid="' + tblparentid + '" data-parentid="' + row.Id + '"><caption>Trace</caption></table>');

        $detail.html(html.join(""));

        DetailSupport.CreateGridTrace($detail.find('#grid5Tbl-' + row.Id));
    };

    this.CreateGrid = function () {
        $("#ClientTblPlaceHolder").replaceWith('<table id="ClientTbl"><caption > Host</caption></table>');
        var table = $("#ClientTbl").bootstrapTable({
            maintainSelected: true,
            pagination: true,
            pageSize: 10,
            uniqueId: 'Id',
            sidePagination: 'client',
            search: true,
            showColumns: true,
            showExport: true,
            exportDataType: 'all',
            exportOptions: { maxNestedTables: 0 },
            exportTypes: ['json', 'xml', 'csv', 'txt', 'excel'],
            detailView: true,
            onExpandRow: DetailSupport.JobTblExpandRow,
            columns: [{
                field: 'Id',
                title: 'Id',
                //formatter: 'UserRelationshipManagerSupport.numeric5_FormatterMaskData',
                sortable: false,
                halign: 'center',
                align: 'right',
                visible: false
            }, {
                field: 'Code',
                title: 'Code',
                sortable: false,
                halign: 'center'
            }, {
                field: 'Name',
                title: 'Name',
                sortable: false,
                halign: 'center'
            }, {
                field: 'Interval',
                title: 'Interval',
                sortable: false,
                halign: 'center'
            },
            {
                field: 'CreateDate',
                title: 'Creado',
                sortable: false,
                halign: 'center'
            },
            {
                field: 'UpdateDate',
                title: 'Actualiado',
                sortable: false,
                halign: 'center'
            }]
        });
    };

    this.CreateGridTrace = function (table) {
        table.bootstrapTable({
            maintainSelected: true,
            pagination: true,
            pageSize: 10,
            uniqueId: 'Id',
            sidePagination: 'client',
            search: true,
            showColumns: true,
            showExport: true,
            exportDataType: 'all',
            exportOptions: { maxNestedTables: 0 },
            exportTypes: ['json', 'xml', 'csv', 'txt', 'excel'],
            columns: [{
                field: 'Id',
                title: 'Id',
                sortable: false,
                halign: 'center',
                align: 'right',
                visible: false
            }, {
                field: 'Message',
                title: 'Message',
                sortable: false,
                halign: 'center'
            }, {
                field: 'Severity',
                    title: 'Severity',
                    formatter: 'DetailSupport.SeverityFormatter',
                sortable: false,
                halign: 'center'
            }, {
                field: 'Successfully',
                title: 'Successfully',
                    formatter: 'DetailSupport.SuccessfullyFormatter',
                sortable: false,
                halign: 'center'
            },
            {
                field: 'URL',
                title: 'URL',
                sortable: false,
                halign: 'center'
            },
            {
                field: 'UpdateDate',
                title: 'Actualiado',
                sortable: false,
                halign: 'center'
            },
            {
                field: 'IP',
                title: 'IP',
                sortable: false,
                halign: 'center'
            },
            {
                field: 'CreateDate',
                title: 'Create',
                sortable: false,
                halign: 'center'
            }]
        });
        DetailSupport.$el = table;
        DetailSupport.TraceLoad();
    };

    this.TraceLoad = function (params) {
        var table = this.$el;
        var row = $('#' + table.data("tblparentid")).bootstrapTable('getRowByUniqueId', table.data("parentid"));
        $.ajax({
            type: 'GET',
            url: constants.URLAPIBase + "trace/TraceByJobId?JobId=" + row.Id,
            dataType: "json",
            data: JSON.stringify({
                filter: ''
            }),
            success: function (data) {
                if (data !== undefined) {
                    table.bootstrapTable('load', data !== null ? data : []);
                }
                else {
                    generalSupport.NotifyFail(data.d.Reason, data.d.Code);
                }
            },
            error: function (qXHR, textStatus, errorThrown) {
                generalSupport.ErrorHandler(qXHR, textStatus, errorThrown);
            }
        });
    };

    this.JobLoad = function (HostId) {
        $.ajax({
            type: 'GET',
            url: constants.URLAPIBase + "job/JobByHostId?HostId=" + HostId,
            dataType: "json",
            data: JSON.stringify({
                filter: ''
            }),
            success: function (data) {
                if (data !== undefined) {
                    $("#ClientTbl").bootstrapTable('load', data !== null ? data : []);
                }
                else {
                    generalSupport.NotifyFail(data.d.Reason, data.d.Code);
                }
            },
            error: function (qXHR, textStatus, errorThrown) {
                generalSupport.ErrorHandler(qXHR, textStatus, errorThrown);
            }
        });
    };

}();

$(document).ready(function () {
    var id = generalManager.GetParameterByName("Id");
    if (id) {
        DetailSupport.CreateGrid();
        DetailSupport.JobLoad(id);
    }
});