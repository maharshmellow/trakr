from django.shortcuts import render
from django.http import HttpResponse
import firebase_admin
from firebase_admin import auth
from firebase_admin import credentials

cred = credentials.Certificate("trakr/keys/trakr-39dff-firebase-adminsdk-h091m-d33131032e.json")
default_app = firebase_admin.initialize_app(cred)


def index(request):
    return render(request, "trakr/mainpage.html")

def home(request):
    return render(request, "trakr/home.html")

def account(request):
    return render(request, "trakr/account.html")

def status(request):
    return render(request, "trakr/status.html")

def logout(request):
    return render(request, "trakr/logout.html")

def getDecodedToken(token):
    # usage: getDecodedToken(token)["uid"] to get the user id
    try:
        return(auth.verify_id_token(token))
    except:
        return False


