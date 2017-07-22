from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie 
import firebase_admin
from firebase_admin import auth
from firebase_admin import credentials
import json
import time
from .api import aws_models
from datetime import datetime

cred = credentials.Certificate("trakr/keys/trakr-39dff-firebase-adminsdk-h091m-d33131032e.json")
default_app = firebase_admin.initialize_app(cred)

@ensure_csrf_cookie
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


def loadUserData(request):
    if request.method == "POST":
        # verify the token
        decoded_token = getDecodedToken(request.POST.get("token"))
        if not decoded_token:
            return HttpResponse(json.dumps({"status":0}))

        # add the user into the database if not there already
        uid = decoded_token["uid"]
        email = decoded_token["email"]

        # see if the user exists
        try:
            user = aws_models.User.get(uid)
            print("User already exists")
        except:
            print("Adding " + uid + " to the database")
            user = aws_models.User(uid=uid, email=email, membership_start=datetime.now())
            user.save()
           
            # get the user information

        # return all information back and add to the render as a json object
        # backend branch test
        return HttpResponse(json.dumps({"status":1, "uid":uid, "email":email, "websites":user.websites}))
