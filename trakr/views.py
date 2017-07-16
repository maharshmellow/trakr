from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def index(request):
    return render(request, "trakr/mainpage.html")


def home(request):
    return render(request, "trakr/home.html")

def account(request):
    return render(request, "trakr/account.html")

def logout(request):
    return render(request, "trakr/logout.html")