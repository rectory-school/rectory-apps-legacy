$(document).ready(function() {
  $("#custom_calendar_dialog").dialog({
    autoOpen: false,
    show: {
      effect: "blind",
      duration: 250
    },
    title: 'Custom Calendar Generator',
  });
  
  $("#custom_calendar_button").click(function(e) {
    $("#custom_calendar_dialog").dialog('open');
    e.preventDefault();
  })
  
  first_day = new Date(); //Today
  first_day.setDate(0); //Last day of last month
  first_day.setDate(first_day.getDate() + 1); //First day of this month
  
  last_day = new Date(); //Today
  last_day.setMonth(first_day.getMonth() + 1); //This day next month
  last_day.setDate(0); //Last day of this month
  
  
  $("#from_date").datepicker({
    changeMonth: true,
    constrainInput: true,
    dateFormat: "yy-mm-dd",
    onClose: function(selectedDate) {
      var date = $.datepicker.parseDate("yy-mm-dd", selectedDate);
      date.setDate(date.getDate() + 1);
      
      $("#to_date").datepicker("option", "minDate", date);
    }
  });
  
  $("#to_date").datepicker({
    changeMonth: true,
    constrainInput: true,
    dateFormat: "yy-mm-dd",
    onClose: function(selectedDate) {
      $("#from_date").datepicker("option", "maxDate", selectedDate);
    }
  });
  
  $("#from_date").datepicker("setDate", first_day);
  $("#to_date").datepicker("setDate", last_day);
})

