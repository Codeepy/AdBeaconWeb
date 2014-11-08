from django.shortcuts import render

def index(request):
    return render(request, "register.html")

def account(request, id):
    return render(request, "account.html")
