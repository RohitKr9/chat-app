from django.shortcuts import render
from .forms import SignUpForm
from django.http import HttpResponse

# Create your views here.
def signup(request):
    
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            return HttpResponse("Your data have been saved", status = 200)
        
    else:
            form = SignUpForm()

    return render(request, "signup.html", {"form": form})
    
def login(request):
    pass
