var recordClicked = false;

$(document).ready(function() {
  $("a.helpLink").on("click", function(e, ui) {

    id = $(this).attr("href")

    $("#" + id).dialog({
      modal: true,
      buttons: {
        Ok: function() {
          $(this).dialog("close");
        }
      }
    });

    e.preventDefault();


  });
  
  $(".btnSave").click(function (e) {
    recordClicked = true;
  });
  
	$(window).bind('beforeunload', function(event) {
		if (! recordClicked) {
			event.stopPropagation();
			event.returnValue = "Warning: You are about to leave this page, but you have not saved your changes. Please scroll to the bottom and click Record my Answers"
			return event.returnValue;
		}
	});
  
});
