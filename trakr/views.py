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
import validators 

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
    # gets the initial data from the logged in user
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

        # return all information back and add to the render as a json object
        return HttpResponse(json.dumps({"status":1, "uid":uid, "email":email, "websites":user.websites}))

def updateWebsites(request):
    # adds or edits the given website for the user and then returns a status code
    if request.method == "POST":
        decoded_token = getDecodedToken(request.POST.get("token"))
        if not decoded_token:
            return HttpResponse(json.dumps({"status":403}))

        # get the website information
        uid = decoded_token["uid"]
        website_name = request.POST.get("website_name")
        website_url = request.POST.get("website_url")
        frequency = request.POST.get("frequency")
        contacts = request.POST.get("contacts").split(",")
        hook_url = request.POST.get("hook_url")

        # error checking
        if not website_name or not website_url or not frequency or not contacts:
            return HttpResponse(json.dumps({"status":400}))
        
        if not validators.url(website_url):
            return HttpResponse(json.dumps({"status":400}))    

        for contact in contacts:
            # check if the contact is a proper email or phone number
            if not contact.isdigit() and not validators.email(contact):
                return HttpResponse(json.dumps({"status":400}))

        if hook_url and not validators.url(hook_url):
            return HttpResponse(json.dumps({"status":400}))
        # update the user data wth the new website
        user = aws_models.User.get(uid)
        old_websites = user.websites
        print("old", old_websites)

        # TODO put the values from the post request here
        website = {website_url:{"name": website_name, "frequency": frequency, "active": 1, "contacts":contacts}}

        # add the new website to the old dictionary
        new_websites = old_websites.copy()
        new_websites.update(website)
        # new_websites = {}     # to clear the data
        print("new", new_websites)
        # if old_websites == new_websites then nothing has changed since the merge handled the duplicates 
        if old_websites != new_websites:
            user.update({"websites":{"value":new_websites, "action":"PUT"}})
            user.refresh()
            print("final", user.websites)

            # TODO add to the websites table 


        return HttpResponse(json.dumps({"status":201}))
        # old_websites += {"https://www.maharsh.net"}

        

        # add the website to the websites table



