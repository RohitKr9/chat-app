from django.contrib.auth import get_user_model, get_user
from django.shortcuts import render
import environ
import datetime

env = environ.Env()
environ.Env.read_env()

User = get_user_model()
users = User.objects.all()

def chatApp(request):

    return render(request, 'index.html')

def chatAppRoom(request, userid):

    requested_user = users.get(id=userid)
    first_name = requested_user.first_name
    last_name = requested_user.last_name
    last_active = requested_user.last_login + datetime.timedelta(seconds=330*60)
    return render(request, 'room.html', {"DOMAIN":env('DOMAIN'),
                                         "first_name":first_name,
                                         "last_name":last_name,
                                         "last_active": last_active
                                         })

def chatHome(request):

    user = get_user(request)
    if user.is_authenticated:
        print(f"Authenticated WebSocket user: {user}")
    else:
        print("WebSocket connection refused: AnonymousUser")
    return render(request, 'chat-home.html', {"users":users})