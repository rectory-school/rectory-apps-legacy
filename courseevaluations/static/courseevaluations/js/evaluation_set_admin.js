$(document).ready(function() {
  $("div.dialog").dialog({
    autoOpen: false,
    show: {
      effect: "blind",
      duration: 250
    },
    width: 800,
    modal: true,
  });
  
  $(".dialog_show_button").click(function(e) {
    target = $(e.currentTarget).attr("href")
    $(target).dialog('open');
    e.preventDefault();
  })
})