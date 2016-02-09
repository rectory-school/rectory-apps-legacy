var doingSave = false;
var originalValues = {};
var updatedValues = {};

$(document).ready(function() {
	setupSaveTrackChange();
	setupLeavePage();
	setupSaveClick();
  setOriginalValues();
  
	setHash(location.hash);
	
	if (location.hash == "#showDates")
		showDates();
	
	if (location.hash == "#showAdvisors")
		showAdvisors();
	
  if (location.hash == "#showWeekdays")
    showWeekdays();
  
	$("#showAdvisor").click(function (e) {
		showAdvisors();
		
		setHash("showAdvisors");
	});
	
	$("#showDates").click(function (e) {
		showDates();
		
		setHash("showDates");
	});
	
	$("#showWeekdays").click(function (e) {
		showWeekdays();
		
		setHash("showWeekdays");
	});
  
	$("#hideOptions").click(function(e) {
		hideOptions();
		
		setHash("")
	});
  
  $("select#massTeacher").change(function(e) {
    val = $(e.currentTarget).val()
    
    $("select.slotSelector").each(function(i, slot) {
      $(slot.options).each(function(i, option) {
        if ($(option).text().startsWith(val)) {
          $(slot).val(option.value);
          $(slot).change();
          return;
        }
      });
      
    });
  })
  
  $("input#checkall").change(function(e) {
    boxes = $("input[type='checkbox'].adminLock")
    boxes.prop('checked', e.currentTarget.checked);
    boxes.change();
  })
  
});

function setOriginalValues() {
  $(".saveTrack").each(function(i, e) {
    checked = e.checked
    
    if (checked != undefined) {
      originalValues[e.name] = checked;
    } else {
      originalValues[e.name] = $(e).val();
    }
    
  })
}

function currentValue(key) {
  if (key in updatedValues) {
    return updatedValues[key];
  }
  
  return originalValues[key];
}

function setHash(hash) {
	location.hash = hash
	
	$('a.hashOption').each(function() {
		this.hash = location.hash;
	});
  
  $('#redirectSavePath').each(function () {
    parts = this.value.split("#");
    url = parts[0]
    
    this.value = url + hash;
  })
}

function setupSaveClick() {
  $(".btnSave").click(function (e) {
    $(".saveTrack").attr('disabled', 'disable');
    $(".btnSave").attr('disabled', 'disabled');
    
    $("#unsavedNotice").hide();
    $("#savedNotice").hide();
    $("#savingNotice").show();
    
    
    var parentForm = $("form#saveData");
    
    $.each(updatedValues, function(key, value) {
      var input = $('<input>');
    
      input.attr('type', 'hidden');
      input.attr('name', key);
      input.attr('value', value);
      input.attr('class', 'hiddenInputForPost');
      
      input.appendTo(parentForm);
    });
    
    e.preventDefault();
		doingSave = true;
    $("form#saveData").submit();
	});
}

function showDates() {
	//Buttons
	$("#showDates").hide();
	$("#showAdvisor").show();
  $("#showWeekdays").show();
	$("#hideOptions").show();
	
	//Lists
	$("div#dates").show();
	$("div#advisors").hide();
  $("div#weekdays").hide();
}

function showAdvisors() {
	//Buttons
	$("#showDates").show();
	$("#showAdvisor").hide();
  $("#showWeekdays").show();
	$("#hideOptions").show();
	
	//Lists
	$("div#dates").hide();
	$("div#advisors").show();
  $("div#weekdays").hide();
}

function showWeekdays() {
	//Buttons
	$("#showDates").show();
	$("#showAdvisor").show();
  $("#showWeekdays").hide();
	$("#hideOptions").show();
	
	//Lists
	$("div#dates").hide();
	$("div#advisors").hide();
  $("div#weekdays").show();
}

function hideOptions() {
	//Buttons
	$("#showDates").show();
	$("#showAdvisor").show();
  $("#showWeekdays").show();
	$("#hideOptions").hide();
	
	//Lists
	$("div#dates").hide();
	$("div#advisors").hide();
  $("div#weekdays").hide();
}

function setupSaveTrackChange() {
  $(".saveTrack").change(function (e) {
    key = e.currentTarget.name;
    
    checked = e.currentTarget.checked;
    
    if (checked != undefined) {
      _newValue = checked
    } else {
      _newValue = e.currentTarget.value;
    }
    
    _originalValue = originalValues[key]
    
    if (_originalValue == _newValue) {
      if (key in updatedValues) {
        delete updatedValues[key];
      }
    } else {
      updatedValues[key] = _newValue;
    }
    
    updateSave();
  });
  
  
  
}

function updateSave() {
  if (Object.keys(updatedValues).length > 0) {
    $(".btnSave").removeAttr('disabled');
    $("p#savedNotice").hide();
    $("p#unsavedNotice").show();
  } else {
    $(".btnSave").attr('disabled', 'disabled');
    $("p#unsavedNotice").hide();
    $("p#savedNotice").show();
  }
}

function setupLeavePage() {	
	$(window).bind('beforeunload', function(event) {
		if (Object.keys(updatedValues).length > 0 && ! doingSave) {
			event.stopPropagation();
			event.returnValue = "Warning: You are about to leave this page, but you have not saved your changes."
			return event.returnValue;
		}
	});
	
}

