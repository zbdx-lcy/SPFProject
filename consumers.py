import json
from channels.generic.websocket import AsyncWebsocketConsumer

class UploadProgressConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("upload_progress", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("upload_progress", self.channel_name)

    async def upload_progress(self, event):
        progress = event["progress"]
        await self.send(text_data=json.dumps({"progress": progress}))
