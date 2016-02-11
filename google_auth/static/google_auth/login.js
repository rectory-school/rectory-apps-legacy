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
  auth2.attachClickHandler(elementID, {}, onSuccess, onError);
}

function onSuccess(googleUser) {
  var profile = googleUser.getBasicProfile();
  
  jQueryAlert("Successfully signed in", profile.getName() + "<br />" + profile.getEmail());
  console.log(googleUser);
  
  alert(Urls["google-auth:login"]())
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