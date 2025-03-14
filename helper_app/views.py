import json

from django.core import serializers
from django.shortcuts import render

# Create your views here.


from django.http import HttpResponse, JsonResponse

from helper_app.models import Chats
from helper_app.models import Messages


def getChatsList(request):
    if request.method == 'GET':
        queryset = Chats.objects.all()
        # 将查询集序列化为 JSON 格式的数据
        chats_list = []
        for item in queryset:
            chats_id = item.id
            title = item.title
            created_at = item.created_at
            updated_at = item.updated_at
            chats_list.append({
                'chat_id': chats_id,
                'title': title,
                'created_at': created_at,
                'updated_at': updated_at
            })

        return JsonResponse({'data': chats_list})
    else:
        return JsonResponse({'error': 'Only GET requests are supported'}, status=405)


def getChatsDetails(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            char_id = data.get('char_id')
            queryset = Messages.objects.filter(char_id_id=char_id)
            messages_list = []
            for item in queryset:
                chats_id = item.chat_id
                title = item.title
                user = item.user
                text = item.text
                created_at = item.created_at
                messages_list.append({
                    'chat_id': chats_id,
                    'title': title,
                    'user': user,
                    'text': text,
                    'created_at': created_at
                })
            messages_list.sort(key=lambda x: x['created_at'])
            return JsonResponse({'data': messages_list})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Can\'t decode JSON'}, status=400)
    else:
        return JsonResponse({'error': 'Only POST requests are supported'}, status=405)
