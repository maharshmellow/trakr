

var config = {
    apiKey: "AIzaSyAiCNv_Pnzrr1l2qUE4zSQiFxqQHMKHspw",
    authDomain: "trakr-39dff.firebaseapp.com",
    databaseURL: "https://trakr-39dff.firebaseio.com",
    projectId: "trakr-39dff",
    storageBucket: "",
    messagingSenderId: "712101225728"
};
firebase.initializeApp(config);

function login(){
    alert("LOGIN - " + document.getElementById("usernameInput").value + " : " + document.getElementById("passwordInput").value);
    console.log();
}

function signup(){
    alert("SIGNUP - " + document.getElementById("usernameInput").value + " : " + document.getElementById("passwordInput").value);

    // create a user on firebase
    username = document.getElementById("usernameInput").value;
    password = document.getElementById("passwordInput").value;

    firebase.auth().createUserWithEmailAndPassword(username, password).catch(function(error) {
      // Handle Errors here.
      var errorCode = error.code;
      var errorMessage = error.message;

      alert(errorCode)
    });
}