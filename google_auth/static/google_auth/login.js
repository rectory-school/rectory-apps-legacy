var googleUser = {};
var googleClientID;
var googleHostedDomain;

$("document").ready(function() {
  googleClientID = $('meta[name=google-signin-client_id]').attr("content");
  googleHostedDomain = $("meta[name=google-signin-hosted_domain]").attr("content");
  
  startGoogleApp();
});

function startGoogleApp() {
  console.log("Google App Started");
  
  gapi.load('auth2',  onAuth2Load);

}

function onAuth2Load() {
  auth2_params = {
    client_id: googleClientID,
    cookiepolicy: 'single_host_origin'
  }
  
  if (googleHostedDomain)
    auth2_params.hosted_domain = googleHostedDomain;
  
  auth2 = gapi.auth2.init(auth2_params);
  attachClickHandler(auth2, "gSignInWrapper")
}

function attachClickHandler(auth2, elementID) {
  auth2.attachClickHandler(elementID, {}, onSuccess, onError);
}

function onSuccess(googleUser) {
document.getElementById('name').innerText = "Signed in: " +
    googleUser.getBasicProfile().getName() + " (" + googleUser.getBasicProfile().getEmail() + ")";
  
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
  div = $("<div/>");
  div.attr("title", title);
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