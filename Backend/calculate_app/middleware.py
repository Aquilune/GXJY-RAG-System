import os
from django.http import JsonResponse

class FileValidationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == '/api/certificates/upload/':
            if 'file' in request.FILES:
                file = request.FILES['file']
                # 检查文件大小 (10MB限制)
                if file.size > 10 * 1024 * 1024:
                    return JsonResponse({
                        'success': False,
                        'error': '文件大小不能超过10MB'
                    }, status=400)
                # 检查文件类型
                if not file.name.lower().endswith(('.xlsx', '.csv')):
                    return JsonResponse({
                        'success': False,
                        'error': '仅支持Excel和CSV格式'
                    }, status=400)
        return self.get_response(request)