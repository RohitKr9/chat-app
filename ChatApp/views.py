from django.contrib.auth import get_user_model
from django.shortcuts import render

User = get_user_model()

def chatApp(request):

    return render(request, 'index.html')

def chatAppRoom(request, userid):
    
    return render(request, 'room.html')

def chatHome(request):

    users = User.objects.all()
    return render(request, 'chat-home.html', {"users":users})