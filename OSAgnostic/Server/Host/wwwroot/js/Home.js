var ManagerSupport = new function () {
    this.IdFormater = function (value, row, index) {
        var valueState = 'green';
        if (value === false) {
            valueState = 'red';
        }
        return '<i class="fas fa-plug ' + valueState + '"></i>';
    };

    this.IdOSSystem = function (value, row, index) {
        var valueState = 'windows';
        if (value === 'Windows') {
            valueState = 'windows';
        } else {
            valueState = 'linux';
        }
        return '<i class="fab fa-' + valueState + '"></i>';
    };

    this.HostTblExpandRow = function (index, row, $detail) {
        var tblparentid = $detail.parent().parent().parent()[0].id;
        var html = [];

        html.push('<table id="grid4Tbl-' + row.Id + '" data-tblparentid="' + tblparentid + '" data-parentid="' + row.Id + '"><caption>Jobs</caption></table>');

        $detail.html(html.join(""));

        ManagerSupport.CreateGridJobs($detail.find('#grid4Tbl-' + row.Id));
    };

    this.JobTblExpandRow = function (index, row, $detail) {
        var tblparentid = $detail.parent().parent().parent()[0].id;
        var html = [];

        html.push('<table id="grid5Tbl-' + row.Id + '" data-tblparentid="' + tblparentid + '" data-parentid="' + row.Id + '"><caption>Trace</caption></table>');

        $detail.html(html.join(""));

        ManagerSupport.CreateGridTrace($detail.find('#grid5Tbl-' + row.Id));
    };

    this.SuccessfullyFormatter

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
                sortable: false,
                halign: 'center'
            }, {
                field: 'Successfully',
                    title: 'Successfully',
                    formatter: 'ManagerSupport.SuccessfullyFormatter',
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
        ManagerSupport.$el = table;
        ManagerSupport.TraceLoad();
    };


    this.TraceLoad = function (params) {
        var table = this.$el;
        var row = $('#' + table.data("tblparentid")).bootstrapTable('getRowByUniqueId', table.data("parentid"));
        $.ajax({
            type: 'GET',
            url: "https://localhost:5001/api/trace?id=" + row.Id,
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

    this.CreateGridJobs = function (table) {
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
            detailView: true,
            onExpandRow: ManagerSupport.JobTblExpandRow,
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
        ManagerSupport.$el = table;
        ManagerSupport.JobsLoad();
    };

    this.JobsLoad = function (params) {
        var table = this.$el;
        var row = $('#' + table.data("tblparentid")).bootstrapTable('getRowByUniqueId', table.data("parentid"));
        $.ajax({
            type: 'GET',
            url: "https://localhost:5001/api/job?id=" + row.Id,
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

    this.CreateGrid = function () {
        $("#ClientTblPlaceHolder").replaceWith('<table id="ClientTbl"><caption > Host</caption></table>');
        $("#ClientTbl").bootstrapTable({
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
            onExpandRow: ManagerSupport.HostTblExpandRow,
            columns: [{
                field: 'Id',
                title: 'Id',
                //formatter: 'UserRelationshipManagerSupport.CustomNumeric_FormatterMaskData',
                sortable: false,
                halign: 'center',
                align: 'right',
                visible: false
            }, {
                field: 'Name',
                title: 'Nombre',
                sortable: false,
                halign: 'center'
            }, {
                field: 'IPLocal',
                title: 'IP Local',
                sortable: false,
                halign: 'center'
            },
            {
                field: 'IPPublic',
                title: 'IP Public',
                sortable: false,
                halign: 'center'
            },
            {
                field: 'MacAddress',
                title: 'Mac Address',
                sortable: false,
                halign: 'center'
            },
            {
                field: 'State',
                title: 'State',
                formatter: 'ManagerSupport.IdFormater',
                sortable: false,
                halign: 'center'
            },
            {
                field: 'OSName',
                title: 'OS Name',
                sortable: false,
                halign: 'center'
            },
            {
                field: 'OSSystem',
                title: 'OS System',
                formatter: 'ManagerSupport.IdOSSystem',
                sortable: false,
                halign: 'center'
            },
            {
                field: 'OSArchitecture',
                title: 'OS Architecture',
                sortable: false,
                halign: 'center'
            }
            ]
        });
    };
    this.MainGridLoad = function () {
        $.ajax({
            type: 'GET',
            url: "https://localhost:5001/api/host",
            dataType: "json",
            data: JSON.stringify({
                filter: ''
            }),
            success: function (data) {
                if (data !== undefined) {
                    $('#ClientTbl').bootstrapTable('load', data !== null ? data : []);
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
};

$(document).ready(function () {
    ManagerSupport.CreateGrid();
    ManagerSupport.MainGridLoad();
});