from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
import firebase_admin
from firebase_admin import auth
from firebase_admin import credentials
import json
from .extras import aws_models
from datetime import datetime
import validators

cred = credentials.Certificate("trakr/keys/trakr-39dff-firebase-adminsdk-h091m-d33131032e.json")
default_app = firebase_admin.initialize_app(cred)

@ensure_csrf_cookie
def index(request):
    return render(request, "trakr/mainpage.html")

def home(request):
    return render(request, "trakr/home.html")

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

        try:
            user = aws_models.User.get(uid)
        except:
            user = aws_models.User(uid=uid, email=email, membership_start=datetime.now())
            user.save()

        return HttpResponse(json.dumps({"status":1, "uid":uid, "email":email, "websites":user.websites}))


def updateWebsites(request):
    # adds or edits the given website for the user
    if request.method == "POST":
        # get the website information
        try:
            decoded_token = getDecodedToken(request.POST.get("token"))
            if not decoded_token:
                return HttpResponse(json.dumps({"status":403}))

            uid = decoded_token["uid"]
            website_name = request.POST.get("website_name")
            website_url = request.POST.get("website_url")

            # validate the information
            if not website_name or not website_url or not validators.url(website_url):
                raise
        except:
            return HttpResponse(json.dumps({"status":400}))

        # update the user data wth the new website
        user = aws_models.User.get(uid)
        old_websites = user.websites

        # maintain the hash, and modified/checked times because we didn't modify that here
        try:
            old_hash = old_websites[website_url]["hash"]
            modified_time = old_websites[website_url]["modified_time"]
            checked_time = old_websites[website_url]["checked_time"]
        except:
            # if the website is new, then we need to initialize the values
            old_hash = ""
            modified_time = "Never"
            checked_time = "Never"

        website = {website_url:{"name": website_name, "modified_time": modified_time, "checked_time":checked_time, "hash":old_hash}}

        # merge the two dictionaries
        if old_websites:
            new_websites = old_websites.copy()
            new_websites.update(website)
        else:
            new_websites = website

        # update the database if there is a change in information
        if old_websites != new_websites:
            user.update({"websites":{"value":new_websites, "action":"PUT"}})
            user.refresh()

        return HttpResponse(json.dumps({"status":201}))

    return HttpResponse(json.dumps({"status":400}))


def deleteWebsite(request):
    if request.method == "POST":
        try:
            decoded_token = getDecodedToken(request.POST.get("token"))
            if not decoded_token:
                return HttpResponse(json.dumps({"status":403}))

            uid = decoded_token["uid"]
            website_url = request.POST.get("website_url")

        except:
            return HttpResponse(json.dumps({"status":400}))


        user = aws_models.User.get(uid)
        websites = user.websites

        if website_url in websites:
            websites.pop(website_url)
            user.update({"websites":{"value":websites, "action":"PUT"}})

        return HttpResponse(json.dumps({"status":201}))

    return HttpResponse(json.dumps({"status":400}))
