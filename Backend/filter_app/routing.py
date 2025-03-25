from django.urls import re_path
from .consumers import ProgressConsumer

websocket_urlpatterns = [
    re_path(r'ws/progress/(?P<task_id>\w+)/$', ProgressConsumer.as_asgi()),  # 这里的 task_id 会传递给消费者
]
