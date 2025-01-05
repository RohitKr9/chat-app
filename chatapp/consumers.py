from channels.generic.websocket import AsyncWebsocketConsumer
import json

class MyConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.group_name = self.room_name

        await self.channel_layer.group_add(
            self.group_name, self.channel_name
        )

        await self.accept()

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        msg = text_data_json["message"]
        print(f"msg recivev {msg}")

        await self.channel_layer.group_send(
            self.group_name,
            {
                "type" : "send_msg",
                "message" : msg
            }
        )
        print("SENT")


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