var config = {
    apiKey: "AIzaSyAiCNv_Pnzrr1l2qUE4zSQiFxqQHMKHspw",
    authDomain: "trakr-39dff.firebaseapp.com",
    databaseURL: "https://trakr-39dff.firebaseio.com",
    projectId: "trakr-39dff",
    storageBucket: "",
    messagingSenderId: "712101225728"
};
firebase.initializeApp(config);

// // main logic 
// firebase.auth().onAuthStateChanged(user => {
//     if (user) {
//         window.location.replace("/home");
//     }
// });

function login() {
    document.getElementById("errorBar").style.visibility = "hidden";
    username = document.getElementById("usernameInput").value;
    password = document.getElementById("passwordInput").value;

    firebase.auth().signInWithEmailAndPassword(username, password).catch(function(error) {
        // var errorCode = error.code;
        // var errorMessage = error.message;

        // alert(errorCode);
        // alert(errorMessage);
        // display the error and clear the password
        document.getElementById("passwordInput").value = "";
        document.getElementById("passwordInput").focus();
        document.getElementById("errorBar").style.visibility = "visible";
    });
}

function signup() {
    document.getElementById("errorBar").style.visibility = "hidden";
    username = document.getElementById("usernameInput").value;
    password = document.getElementById("passwordInput").value;

    firebase.auth().createUserWithEmailAndPassword(username, password).catch(function(error) {
        // Handle Errors here.
        // var errorCode = error.code;
        // var errorMessage = error.message;

        // alert(errorCode)
        document.getElementById("usernameInput").value = "";
        document.getElementById("passwordInput").value = "";
        document.getElementById("usernameInput").focus();
        document.getElementById("errorBar").style.visibility = "visible";
    });
}

function signout() {
    firebase.auth().signOut().then(function() {
        window.location.replace("/");
        // TODO go back to the main page
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


