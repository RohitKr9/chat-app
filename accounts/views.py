from django.shortcuts import render
from .forms import SignUpForm
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.contrib.auth import get_user

# Create your views here.
def signup(request):
    
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            print("FORM VALIDATED")
            print(request.POST["email"])
            print(request.POST["first_name"])
            print(request.POST["last_name"])
            print(request.POST["password"])
            form.save()
            return HttpResponseRedirect(reverse('chat_home'))
        
    else:
            print("FORM NOT VALIDATED")
            form = SignUpForm()

    return render(request, "signup.html", {"form": form})
    

def loginUser(request):
    
    if request.method == 'POST':
        data = request.POST
        print(data["email"])
        print(data["password"])
        user = authenticate(username = data["email"], password = data["password"])
        
        
        if user is not None:
            login(request, user)
            print(f"User in not None inside loginuser view: {user}, is_authenticated: {user.is_authenticated}")
            return HttpResponseRedirect(reverse('chat_home'))

    return render(request, "login.html", {"session_id":request.session.session_key})