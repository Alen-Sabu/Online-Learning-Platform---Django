import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NotificationConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        """This method is called when a WebSocket connection is establised
        """
        self.user = self.scope["user"]
        if self.user.is_anonymous:
            await self.close()
        else:
             await self.channel_layer.group_add(
                 f"user_{self.user.id}",
                 self.channel_name
             )
             await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            f"user_{self.user.id}",
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)

    async def send_notification(self, event):
        await self.send(text_data=json.dumps(event["message"]))
