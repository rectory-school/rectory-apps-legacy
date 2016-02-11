var googleUser = {};
var googleClientID;
var googleHostedDomain;

$("document").ready(function() {
  googleClientID = $('meta[name=google-signin-client_id]').attr("content");
  googleHostedDomain = $("meta[name=google-signin-hosted_domain]").attr("content");
  
  var autoOpenDialog = ($("meta[name=start_django_form]").length > 0)
  
  $("#django-signon").click(function(e) {
    $("#django-signon-form").dialog("open");
  })
  
  $("#django-signon-form").dialog({
    autoOpen: autoOpenDialog,
    width: 500,
    movable: false,
  })
  
  var csrftoken = $.cookie('csrftoken');
  
  $.ajaxSetup({
      beforeSend: function(xhr, settings) {
          if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
              // Send the token to same-origin, relative URLs only.
              // Send the token only if the method warrants CSRF protection
              // Using the CSRFToken value acquired earlier
              xhr.setRequestHeader("X-CSRFToken", csrftoken);
          }
      }
  });
  
  startGoogleApp();
});

function startGoogleApp() {
  console.log("Google App Started");
  
  gapi.load('auth2',  onAuth2Load);

}

function onAuth2Load() {
  var auth2_params = {
    client_id: googleClientID,
    cookiepolicy: 'single_host_origin'
  }
  
  if (googleHostedDomain)
    auth2_params.hosted_domain = googleHostedDomain;
  
  var auth2 = gapi.auth2.init(auth2_params);
  attachClickHandler(auth2, "google-signon");
}

function attachClickHandler(auth2, elementID) {
  auth2.attachClickHandler(elementID, {}, onGoogleLoginSuccess, onError);
}

function onGoogleLoginSuccess(googleUser) {
  var processURL = Urls["google-auth:login"]()
  
  $.post({
    url: processURL,
    data: {'id_token': googleUser.getAuthResponse().id_token, logon_type: 'google'},
    success: onDjangoLoginSuccess
  });
}

function onDjangoLoginSuccess(data) {
  window.location = $("meta[name=next]").attr("content");
}

function onError(error) {
  console.log(error);
  
  if (googleHostedDomain && error.type == "tokenFailed" && error.accountDomain != error.expectedDomain) {
    jQueryAlert("Error Logging In", "Please make sure you are using your " + googleHostedDomain + " account")
  } else {
    jQueryAlert("There was an error processing your request. Please reload the page and try again.");
  }
}

function jQueryAlert(title, message) {
  var div = $("<div/>");
  div.attr("title", title);
  div.attr("class", "dialog-alert");
  
  div.html(message);
  
  div.dialog({
    modal: true,
    draggable: false,
    buttons: {
      Ok: function() {
        $(this).dialog("close");
      }
    }
  }); 
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
}