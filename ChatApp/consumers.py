from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from accounts.models import Message
import json
from django.contrib.auth import get_user_model
from django_redis import get_redis_connection
from msgpack import packb, unpackb
import datetime

redis_client = get_redis_connection("default")
User = get_user_model()

class MyConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        
        user = self.scope['user']
        session = self.scope.get("session")

        print(f"User in WebSocket: {user}, is_authenticated: {user.is_authenticated}")
        print(f"Session: {session}")

        # Ensure user is authenticated
        if not user.is_authenticated:
            print("Unauthenticated user, closing WebSocket.")
            await self.close(code=4001)
            return

        self.user_id_1 = user.id

        # Ensure 'userid' is present and valid
        try:
            self.user_id_2 = int(self.scope["url_route"]["kwargs"].get("userid"))
        except (TypeError, ValueError):
            print("Invalid or missing userid, closing WebSocket.")
            await self.close(code=4002)
            return

        print(f"USER 1 ID: {self.user_id_1}")
        print(f"USER 2 ID: {self.user_id_2}")

        # Create room name
        self.room_name = f"{min(self.user_id_1, self.user_id_2)}-{max(self.user_id_1, self.user_id_2)}"
        self.group_name = self.room_name
        print(f"Room Name: {self.room_name}")

        await self.channel_layer.group_add(
           self.group_name, self.channel_name
        )

        # Accept the WebSocket connection
        await self.accept()


    async def receive(self, text_data):
        text_data_dict = json.loads(text_data)
        msg = text_data_dict["message"]
        self.msg_user_id = self.scope['user'].id

        await self.channel_layer.group_send(
            self.group_name,
            {
                "type" : "send_msg",
                "message" : {
                    "message_recived" : msg,
                    "userid" : self.msg_user_id
                }
            }
        )
        await sync_to_async(self.message_store)(msg)
        print(f"sent for saving message")
    

    async def send_msg(self, event):
        msg = event["message"]

        print(f"sending msg {msg}")

        await self.send(text_data=json.dumps({
            "message": msg
        }))

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.group_name,  self.channel_name
        )

    def message_store(self,message):

        sender = User.objects.get(id=self.user_id_1)
        receiver =  User.objects.get(id=self.user_id_2)
        print(sender)
        print(receiver)
        message_text = str(message)
        message_to_store = Message(
            sender = sender,
            receiver =  receiver,
            message = message
        )
        message_to_store.save()
        self.cache_store(message)

        #we will store to redis cache
    def cache_store(self, message):
        list_name = self.room_name
        cache_msg = packb(
            {
                "sender": self.msg_user_id,
                "timestamp" : datetime.datetime.now().isoformat(),
                "message": message
            }
        )
        if (redis_client.llen(list_name) > 10):
            redis_client.rpop(list_name)
        redis_client.lpush(list_name, cache_msg) 
        msgs = redis_client.lrange(list_name, 0, -1)
        for m in msgs:
            last_msg = unpackb(m)
            print(last_msg)   