from django.contrib.auth import get_user_model, get_user
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
import environ
import datetime
import json


env = environ.Env()
environ.Env.read_env()

User = get_user_model()
users = User.objects.all()

def chatApp(request):

    return render(request, 'index.html')

@login_required
def chatAppRoom(request, userid):

    #load all the message
    #here you need to load the last 50 chats from db and loads the cache

    #get messages from cache
    # msg_cache_raw = cache.get_client().zrange("messages", 0, -1)
    # message_dict = [json.loads(msg.decode("utf-8")) for msg in msg_cache_raw]
    
    requested_user = users.get(id=userid)
    first_name = requested_user.first_name
    last_name = requested_user.last_name
    last_active = requested_user.last_login + datetime.timedelta(seconds=330*60)
    return render(request, 'room.html', {"DOMAIN":env('DOMAIN'),
                                         "first_name":first_name,
                                         "last_name":last_name,
                                         "last_active": last_active
                                        #  "messages": json.dumps(message_dict)
                                         })

@login_required
def chatHome(request):

    user = get_user(request)
    other_users = users.exclude(id = user.id)
    print(user.id)
    print(user)
    return render(request, 'chat-home.html', {"users":other_users})