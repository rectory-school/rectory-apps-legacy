$(document).ready(function() {
	$("a.helpLink").on("click", function(e, ui) {
		
		id = $(this).attr("href")
		
		$("#" + id).dialog({
		      modal: true,
			  buttons: {
			      Ok: function() {
			          $( this ).dialog( "close" );
			      }
			  }
		    });
			
		e.preventDefault();
		
		
	});
});