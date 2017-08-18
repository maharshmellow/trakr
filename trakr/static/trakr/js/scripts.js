var config = {
    apiKey: "AIzaSyAiCNv_Pnzrr1l2qUE4zSQiFxqQHMKHspw",
    authDomain: "trakr-39dff.firebaseapp.com",
    databaseURL: "https://trakr-39dff.firebaseio.com",
    projectId: "trakr-39dff",
    storageBucket: "",
    messagingSenderId: "712101225728"
};
firebase.initializeApp(config);

function login() {
    document.getElementById("errorBar").style.visibility = "hidden";
    document.getElementById("errorBar").innerHTML = "Invalid"

    username = document.getElementById("usernameInput").value;
    password = document.getElementById("passwordInput").value;

    firebase.auth().signInWithEmailAndPassword(username, password).catch(function(error) {
        document.getElementById("passwordInput").value = "";
        document.getElementById("passwordInput").focus();
        document.getElementById("errorBar").style.visibility = "visible";
    });
}

function signup() {
    document.getElementById("errorBar").style.visibility = "hidden";
    document.getElementById("errorBar").innerHTML = "Invalid"

    username = document.getElementById("usernameInput").value;
    password = document.getElementById("passwordInput").value;

    firebase.auth().createUserWithEmailAndPassword(username, password).catch(function(error) {
        if (error.code == "auth/email-already-in-use"){
            document.getElementById("errorBar").innerHTML = "Email already in use"
        }
        else if (error.code == "auth/weak-password"){
            document.getElementById("errorBar").innerHTML = "Weak Password"
        }
        document.getElementById("usernameInput").value = "";
        document.getElementById("passwordInput").value = "";
        document.getElementById("usernameInput").focus();
        document.getElementById("errorBar").style.visibility = "visible";
    });
}

function signout() {
    firebase.auth().signOut().then(function() {
        window.location.replace("/");
    }, function(error) {
        console.error('Sign Out Error', error);
    });
}


function getCurrentUserToken() {
    firebase.auth().currentUser.getIdToken().then(function(idToken) {
        return (idToken);
    }).catch(function(error) {
        signout();
    });
    return (null);
}

//For getting CSRF token
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

function setInfoMessage(message) {
    document.getElementById("infoMessage").style.display = "block";
    document.getElementById("infoMessage").innerHTML = message;
}

function removeInfoMessage(){
    document.getElementById("infoMessage").style.display = "none";
}

function logout(){
    alert("test");
}
