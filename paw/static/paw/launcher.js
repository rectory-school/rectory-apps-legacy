function clickDialog(e) {
	toShow = $(e.currentTarget).attr("href")
	
	var count = $(toShow).find(".entry").length

  $(toShow).dialog({height: $(window).height() - 50})
  $(toShow).dialog({width: $(window).width() - 50})
  
	$(toShow).dialog("open");

	$(".dialogHide").hide();
	
	return false;
}

function dismissDialog(e, ui) {
	$(".dialogHide").show();
}

$(document).ready(function() {
	$( ".dialog" ).dialog({
		autoOpen: false,
		show: {
			effect: "blind",
			duration: 500},
		hide: {
			effect: "fade",
			duration: 250},
		height: 700,
		width: 700,
		modal: true,
		beforeClose: dismissDialog});

	$("a.dialogLauncher").click(clickDialog);
  $(".startHidden").hide();
  checkURLTick();
});

function checkURLTick() {
  checkAllURLs();
  
  setTimeout(checkURLTick, 10000);
}

function checkAllURLs() {
  urls = getCheckURLs();
  
  $(urls).each(function(i, url) { checkURL(url); });
}

function getCheckURLs() {
  return $.unique(
    $("div[data-check-url]").map(function() {
      return $(this).data("checkUrl")
    })
  )
}

function checkURL(url) {
  var request = $.ajax({
    url: url,
    type: "GET",
    dataType: "text"
  });
  
  request.success(function() {
    showByCheckURL(url);
  });
  
  request.fail(function() {
    hideByCheckURL(url);
  });
}

function showByCheckURL(url) {
  getByCheckURL(url).show();
}

function hideByCheckURL(url) {
  getByCheckURL(url).hide();
}

function getByCheckURL(url){
  selector = "div[data-check-url='" + url + "']"
  return $(selector)
}