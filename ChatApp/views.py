from django.contrib.auth import get_user_model, get_user
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
import environ
import datetime
from django_redis import get_redis_connection
from msgpack import unpackb


env = environ.Env()
environ.Env.read_env()

User = get_user_model()
users = User.objects.all()

def chatApp(request):

    return render(request, 'index.html')

@login_required
def chatAppRoom(request, userid):

    user = get_user(request=request)
    redis_client = get_redis_connection("default")
    cache_list = f"{min(user.id, userid)}-{max(user.id, userid)}"
    print(cache_list)

    msg_list_byte = redis_client.lrange(cache_list, 0, -1)
    msgs_list = []
    for msg in msg_list_byte:
        msg_str = unpackb(msg)
        print("this is testing of tyPPEEPEPE")
        print(type(msgs_list))
        msgs_list.append(msg_str)
    
    # msgs_json_string = f"[{msgs_json_string}]"
    
    requested_user = users.get(id=userid)
    first_name = requested_user.first_name
    last_name = requested_user.last_name
    
    user.last_login = datetime.datetime.now()
    user.save()

    last_active = requested_user.last_login + datetime.timedelta(seconds=330*60)
    
    return render(request, 'room.html', {"DOMAIN":env('DOMAIN'),
                                         "first_name":first_name,
                                         "last_name":last_name,
                                         "last_active": last_active,
                                         "messages": reversed(msgs_list)
                                         })

@login_required
def chatHome(request):

    user = get_user(request)
    other_users = users.exclude(id = user.id)
    print(user.id)
    print(user)
    return render(request, 'chat-home.html', {"users":other_users})