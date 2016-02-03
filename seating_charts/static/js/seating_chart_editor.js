var inProcess = 0;

$(document).ready(function() {
	function getCookie(name) {
	    var cookieValue = null;
	    if (document.cookie && document.cookie != '') {
	        var cookies = document.cookie.split(';');
	        for (var i = 0; i < cookies.length; i++) {
	            var cookie = jQuery.trim(cookies[i]);
	            // Does this cookie string begin with the name we want?
	            if (cookie.substring(0, name.length + 1) == (name + '=')) {
	                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
	                break;
	            }
	        }
	    }
	    return cookieValue;
	}
	
	var csrftoken = getCookie('csrftoken');
	
	function csrfSafeMethod(method) {
	    // these HTTP methods do not require CSRF protection
	    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
	}
	$.ajaxSetup({
	    crossDomain: false, // obviates need for sameOrigin test
	    beforeSend: function(xhr, settings) {
	        if (!csrfSafeMethod(settings.type)) {
	            xhr.setRequestHeader("X-CSRFToken", csrftoken);
	        }
	    }
	});
	
	reloadData();
	fixSizes();
	updateStatus();
	
	var $sidebar   = $("#leftovers"), 
	        $window    = $(window),
	        offset     = $sidebar.offset(),
	        topPadding = 15;

	    $window.scroll(function() {
	        if ($window.scrollTop() > offset.top) {
	            $sidebar.stop().animate({
	                marginTop: $window.scrollTop() - offset.top + topPadding
	            });
	        } else {
	            $sidebar.stop().animate({
	                marginTop: 0
	            });
	        }
	    });
	
		$(window).bind('beforeunload', function(event) {
			if (inProcess > 0) {
				event.stopPropagation();
				event.returnValue = "Warning: There are currently unsaved changes. Are you sure you want to close the page? The recommendation is to wait until all changes are saved before closing."
				return event.returnValue;
			}
		});
});

$(window).resize(fixSizes);

function fixSizes() {
	width = $(window).width();
	tablesSize = width - 250;
	$("div#tables").width(tablesSize);
	console.log(width);
}

function makeSortable() {
	$("ul").sortable({
      connectWith: ".connected",
	  receive: handleMoveStudent,
      cancel: ".ui-state-disabled" 
    }).disableSelection();
}

function handleMoveStudent(event, ui) {
	studentID = ui.item.data("student_id");
	parentUL = ui.item.parent();
	
	ui.item.addClass('ui-state-disabled');
	
	if (parentUL == $("ul#leftovers")) {
		moveStudent(studentID, null);
	} else {
		moveStudent(studentID, parentUL.data("table_id"), function() {ui.item.removeClass('ui-state-disabled')});
	}
}

function reloadData() {
	console.log("reloadData");
	
	$("div#tables div").remove();
	$("div#leftovers li").remove();
	$.get(Urls.seating_chart_data(id=MEALTIMEID), {}, processData, 'json' );
}

function moveStudent(studentID, tableID, success) {
	inProcess++;
	updateStatus();
	console.log("Moving student " + studentID + " to " + tableID);
	$.post(Urls.seating_chart_move(id=MEALTIMEID), {student_id: studentID, table_id: tableID}, function() {inProcess--; updateStatus(); success();});
}

function updateStatus() {
	if (inProcess == 0) {
		$("#status").text("There are no operations in processing, this window is safe to close");
	}
	
	if (inProcess == 1) {
		$("#status").text("There is 1 operation still in processing, please do not close this window");
	}
	
	if (inProcess > 1) {
		$("#status").text("There are " + inProcess + " operations still in process, please do not close this window");
	}
}

function processData(data) {
	console.log("processData", data);
	$(data.tables).each(function(i) {
		table = this;
		div = $(document.createElement('div'))
		ul = $(document.createElement('ul'))
		h = $(document.createElement('h1'));
		h.text(table.description);
		div.append(h);
		div.addClass('table');
		ul.addClass('connected');
		ul.addClass('table');
		ul.data('table_id', table.id);
		
		$(table.fillers).each(function(i) {
			filler = this;
			
			p = $(document.createElement('p'));
			p.text(filler.description + " (" + filler.seats + ")");
			div.append(p);
		});
		
		$(table.students).each(function(i) {
			student = this;
			
			li = $(document.createElement('li'));
			li.data('student_id', student.id);
			li.text(student.first_name + " " + student.last_name);
			ul.append(li);
		});
		
		div.append(ul);
		$("div#tables").append(div);
	});
	
	console.log(data.leftovers);
	
	leftovers = $("ul#leftovers");
	$(data.leftovers).each(function(i) {
		student = this;
		
		li = $(document.createElement('li'));
		li.data('student_id', student.id);
		li.text(student.first_name + " " + student.last_name);
		leftovers.append(li);
	});
	
	makeSortable();
}