
from django.shortcuts import render

def chatApp(request):

    return render(request, 'index.html')

def chatAppRoom(request, room_name):

    return render(request, 'room.html')