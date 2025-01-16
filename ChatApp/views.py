from django.contrib.auth import get_user_model, get_user
from django.shortcuts import render
import environ

env = environ.Env()
environ.Env.read_env()

User = get_user_model()

def chatApp(request):

    return render(request, 'index.html')

def chatAppRoom(request, userid):

    return render(request, 'room.html', {"DOMAIN":env('DOMAIN')})

def chatHome(request):

    users = User.objects.all()
    user = get_user(request)
    if user.is_authenticated:
        print(f"Authenticated WebSocket user: {user}")
    else:
        print("WebSocket connection refused: AnonymousUser")
    return render(request, 'chat-home.html', {"users":users})