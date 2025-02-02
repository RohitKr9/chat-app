from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from accounts.models import Message
import json
from django.contrib.auth import get_user_model

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

        await self.channel_layer.group_send(
            self.group_name,
            {
                "type" : "send_msg",
                "message" : {
                    "message_recived" : msg,
                    "userid" :self.scope['user'].id
                }
            }
        )
        await sync_to_async(self.message_store)(msg)
    

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
        message = Message(
            sender = User.objects.get(id=self.user_id_1),
            receiver =  User.objects.get(id=self.user_id_2),
            message = message
        )
        message.save()