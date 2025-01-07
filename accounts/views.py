from django.shortcuts import render
from .forms import SignUpForm
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate
from django.urls import reverse
import json

# Create your views here.
def signup(request):
    
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            print(request.POST["email"])
            print(request.POST["first_name"])
            print(request.POST["last_name"])
            print(request.POST["password"])
            form.save()
            return HttpResponseRedirect(reverse('chat_home'))
        
    else:
            form = SignUpForm()

    return render(request, "signup.html", {"form": form})
    

def login(request):
    
    if request.method == 'POST':
        data = request.POST
        print(data["email"])
        print(data["password"])
        user = authenticate(username = data["email"], password = data["password"])
        print(user)

        if user is not None:
            return HttpResponseRedirect(reverse('chat_home'))

    return render(request, "login.html")