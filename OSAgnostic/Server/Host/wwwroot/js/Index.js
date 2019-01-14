var ManagerSupport = new function() {
  this.URLBase = "https://localhost:5005/api/";
  this.Template =
    '<div class="col-2"> ' +
    '<div class="card" id="Host{Id}" name="Host{Id}"> ' +
    "	<h5>{Name}</h5>" +
    '	<i class="fa fa-{OSSystemIcon}"></i>' +
    '	<p class="title">{OSSystem}</p>' +
    "	<p>IP Public:{IPPublic}</p>" +
    "	<p>IP Local:{IPLocal}</p>" +
    '	<div style="margin: 24px 0;">' +
    '		<a href="#"><i id="Host{Id}State" name="Host{Id}State" class="fa fa-plug {Plug}"></i></a>' +
    "	</div>" +
    "	<p><button>Jobs</button></p>" +
    "</div>" +
    "</div>";

  this.BuilderItem = function(value) {
    var itemTemplate = ManagerSupport.Template.replace("{Name}", value.Name);

    var valueOSSystem = "windows";
    if (value.OSSystem === "Windows") {
      valueOSSystem = "windows";
    } else {
      valueOSSystem = "linux";
    }

    var valueState = "_green";
    if (value.State === false) {
      valueState = "_red";
    }

    itemTemplate = itemTemplate.replace("{Id}", value.Id);
    itemTemplate = itemTemplate.replace("{Id}", value.Id);
    itemTemplate = itemTemplate.replace("{Id}", value.Id);
    itemTemplate = itemTemplate.replace("{Id}", value.Id);
    itemTemplate = itemTemplate.replace("{OSSystem}", value.OSSystem);

    itemTemplate = itemTemplate.replace("{OSSystemIcon}", valueOSSystem);
    itemTemplate = itemTemplate.replace("{IPPublic}", value.IPPublic);
    itemTemplate = itemTemplate.replace("{IPLocal}", value.IPLocal);
    itemTemplate = itemTemplate.replace("{Plug}", valueState);

    return itemTemplate;
  };

  this.HostUpdate = function() {
    $.ajax({
      type: "GET",
      url: ManagerSupport.URLBase + "host",
      dataType: "json",
      data: JSON.stringify({
        filter: ""
      }),
      success: function(data) {
        if (data !== undefined) {
          $.each(data, function(index, value) {
            if ($("#Host" + value.Id + "State").length) {
              var valueState = "_green";
              if (value.State === false) {
                valueState = "_red";
              }

              var oldValue = $("#Host" + value.Id + "State").prop("class");
              $("#Host" + value.Id + "State").removeClass();
              $("#Host" + value.Id + "State").addClass(
                "fa fa-plug " + valueState
              );
              $("#Host" + value.Id + "State").addClass("animated rubberBand");
              if (oldValue.indexOf(valueState) === -1) {
                window.setTimeout(function() {
                  $("#Host" + value.Id + "State").removeClass(
                    "animated rubberBand"
                  );
                }, 3000);
              } else {
                $("#Host" + value.Id + "State").removeClass(
                  "animated rubberBand"
                );
              }
            } else {
              var itemTemplate = ManagerSupport.BuilderItem(value);
              $("#Container").append(itemTemplate);
            }
          });
        } else {
          generalSupport.NotifyFail(data.d.Reason, data.d.Code);
        }
      },
      error: function(qXHR, textStatus, errorThrown) {
        generalSupport.ErrorHandler(qXHR, textStatus, errorThrown);
      }
    });
  };

  this.MainGridLoad = function() {
    $.ajax({
      type: "GET",
      url: ManagerSupport.URLBase + "host",
      dataType: "json",
      data: JSON.stringify({
        filter: ""
      }),
      success: function(data) {
        if (data !== undefined) {
          $.each(data, function(index, value) {
            var itemTemplate = ManagerSupport.BuilderItem(value);
            $("#Container").append(itemTemplate);
          });
        } else {
          generalSupport.NotifyFail(data.d.Reason, data.d.Code);
        }
      },
      error: function(qXHR, textStatus, errorThrown) {
        generalSupport.ErrorHandler(qXHR, textStatus, errorThrown);
      }
    });
  };
}();

$(document).ready(function() {
  $.periodic({ period: 20000, decay: 1.2, max_period: 60000 }, function() {
    ManagerSupport.HostUpdate();
  });

  ManagerSupport.MainGridLoad();
});
