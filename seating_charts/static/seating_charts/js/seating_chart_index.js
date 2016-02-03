$(document).ready(function() {
	$(".shuffleConfirm").on('click', function(e) {
		console.log(e);
		
		ok = confirm("Warning: You are about to shuffle the meal \"" + e.toElement.text + "\".\n\nYou cannot undo this after proceeding.");
		
		if (! ok)
			e.preventDefault();
	})
})