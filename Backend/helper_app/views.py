import json

import numpy as np
from django.core import serializers
from django.shortcuts import render


from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ollama import embeddings
from torch import cosine_similarity

from helper_app.models import Chats, VectorData
from helper_app.models import Messages
from .configuration import OLLAMA_URL, MODEL_NAME


@csrf_exempt
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

@csrf_exempt
def getChatsDetails(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            index = data.get('index')
            queryset = Messages.objects.filter(chat_id=index)
            serialized_data = serializers.serialize('python', queryset)
            messages_list = []
            for item in serialized_data:
                fields = item['fields']
                messages_list.append({
                    'chat_id': fields['chat_id'],
                    'user': fields['user'],
                    'text': fields['text'],
                    'created_at': fields['created_at'].strftime('%Y-%m-%d %H:%M:%S')
                })
            messages_list.sort(key=lambda x: x['created_at'])
            return JsonResponse({'data': messages_list})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Can\'t decode JSON'}, status=400)
    else:
        return JsonResponse({'error': 'Only POST requests are supported'}, status=405)

import requests
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import KnowledgeBaseFile, VectorData
from sentence_transformers import SentenceTransformer
from django.conf import settings
import PyPDF2
import json

# # 初始化 SentenceTransformer 模型
# model = SentenceTransformer('all-MiniLM-L6-v2')
#
# # 添加文件接口
# @csrf_exempt
# def add_file(request):
#     if request.method == 'POST' and 'file' in request.FILES:
#         file_ids = []
#         try:
#             # 遍历所有上传的文件
#             for file in request.FILES.getlist('file'):
#                 # 保存文件到数据库
#                 knowledge_base_file = KnowledgeBaseFile(file=file)
#                 knowledge_base_file.save()
#                 file_ids.append(knowledge_base_file.id)
#
#                 file_path = os.path.join(settings.MEDIA_ROOT, str(knowledge_base_file.file))
#                 # 判断文件类型
#                 if file.name.lower().endswith('.pdf'):
#                     # 处理 PDF 文件
#                     with open(file_path, 'rb') as f:
#                         pdf_reader = PyPDF2.PdfReader(f)
#                         content = ""
#                         for page in pdf_reader.pages:
#                             content += page.extract_text()
#                         print('content:' + content)
#                 else:
#                     # 处理文本文件
#                     with open(file_path, 'r', encoding='utf-8') as f:
#                         content = f.read()
#
#                 # 将文件内容分割成段落
#                 paragraphs = content.split('\n\n')
#
#                 # 将段落添加到向量数据库
#                 for i, para in enumerate(paragraphs):
#                     # 生成向量
#                     vector = model.encode(para)
#                     vector_json = json.dumps(vector.tolist())
#
#                     # 保存段落和向量到数据库
#                     VectorData.objects.create(
#                         file=knowledge_base_file,
#                         paragraph=para,
#                         vector=vector_json
#                     )
#
#             return JsonResponse({'message': '文件添加成功', 'file_ids': file_ids}, status=200)
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=500)
#     return JsonResponse({'error': '无效的请求，请提供文件'}, status=400)

# 对话接口
from sentence_transformers import SentenceTransformer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from.models import KnowledgeBaseFile, VectorData
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import requests
#
# @csrf_exempt
# def chat(request):
#     print("执行了")
#     if request.method == 'POST':
#         data = request.POST
#         question = data.get('question')
#
#         if question:
#             # 生成问题的向量
#             question_vector = model.encode(question)
#
#             # 从 MySQL 中检索所有段落和向量
#             all_vector_data = VectorData.objects.all()
#             relevant_docs = []
#             similarities = []
#
#             for vector_data in all_vector_data:
#                 # 从数据库中获取向量并转换为列表
#                 stored_vector = eval(vector_data.vector)
#                 # 计算余弦相似度
#                 similarity = cosine_similarity([question_vector], [stored_vector])[0][0]
#                 similarities.append(similarity)
#                 relevant_docs.append(vector_data.paragraph)
#
#             # 根据相似度排序并选择前 2 个相关文档
#             sorted_indices = np.argsort(similarities)[::-1]
#             top_2_docs = [relevant_docs[i] for i in sorted_indices[:2]]
#
#             # 构建包含问题和相关文档的提示
#             prompt = f"问题: {question}\n相关信息: {' '.join(top_2_docs)}"
#
#             # 调用 Ollama API
#             ollama_url = OLLAMA_URL
#             payload = {
#                 "model": MODEL_NAME,
#                 "prompt": prompt,
#                 "stream": False
#             }
#             try:
#                 response = requests.post(ollama_url, json=payload)
#                 if response.status_code == 200:
#                     result = response.json()
#                     answer = result.get('response', '未找到有效回答。')
#                     return JsonResponse({'answer': answer})
#                 else:
#                     return JsonResponse({'error': f'请求 Ollama 失败，状态码: {response.status_code}，错误信息: {response.text}'}, status=500)
#             except requests.RequestException as e:
#                 return JsonResponse({'error': str(e)}, status=500)
#         return JsonResponse({'error': '请提供问题'}, status=400)
#     return JsonResponse({'error': '无效的请求方法，仅支持 POST 请求'}, status=405)