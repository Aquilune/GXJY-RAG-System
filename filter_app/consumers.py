from channels.generic.websocket import AsyncWebsocketConsumer
import json
import logging
logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ProgressConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.task_id = self.scope['url_route']['kwargs']['task_id']
        logger.info(f"WebSocket连接建立，task_id: {self.task_id}，完整URL可能为ws://your_domain/ws/progress/{self.task_id}/")
        self.group_name = f'progress_{self.task_id}'
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # 离开组
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def send_progress(self, event):
        progress = event['progress']
        # 发送消息给 WebSocket 客户端
        await self.send(text_data=json.dumps({
            'progress': progress
        }))