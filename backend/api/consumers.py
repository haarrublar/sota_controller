import json
from channels.generic.websocket import AsyncWebsocketConsumer


class ControllerConsumer(AsyncWebsocketConsumer):
  GROUP_NAME = "controller_group"

  async def connect(self):
    await self.channel_layer.group_add(self.GROUP_NAME, self.channel_name)
    await self.accept()

  async def disconnect(self, close_code):
    await self.channel_layer.group_discard(self.GROUP_NAME, self.channel_name)

  async def receive(self, text_data):
    data = json.loads(text_data)
    
    if data.get("action") == "SELECT_COLOR":
        selected_color = data.get("color")
        print("Received in Django:", selected_color)

    await self.channel_layer.group_send(
        self.GROUP_NAME, {"type": "broadcast_event", "payload": data}
    )

  async def broadcast_event(self, event):
    await self.send(text_data=json.dumps(event["payload"]))