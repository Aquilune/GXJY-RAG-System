from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CottonConfig, CottonCertificate, CalculationResult
from django.core.exceptions import ValidationError
from datetime import datetime

from .serializers import CertificateUploadSerializer


@csrf_exempt
def cotton_config_view(request, config_id=None):
    try:
        if request.method == 'GET':
            return handle_get(request, config_id)
        elif request.method == 'POST':
            return handle_post(request)
        elif request.method == 'DELETE':
            return handle_delete(request, config_id)
        else:
            return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }, status=500)


def handle_get(request, config_id):
    """处理GET请求"""
    if config_id:
        # 获取单个配置详情
        try:
            config = CottonConfig.objects.get(id=config_id)
            return JsonResponse({
                'success': True,
                'data': {
                    'id': config.id,
                    'name': config.name,
                    'length_strength_params': config.length_strength_params,
                    'micronaire_params': config.micronaire_params,
                    'hand_machine_length_params': config.hand_machine_length_params,
                    'processing_quality_params': config.processing_quality_params,
                    'origin_params': config.origin_params,
                    'fiber_quality_params': config.fiber_quality_params,
                    'rejection_criteria': config.rejection_criteria,
                    'policy_params': config.policy_params,
                    'created_at': config.created_at.isoformat(),
                    'updated_at': config.updated_at.isoformat()
                }
            })
        except CottonConfig.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': f'Configuration with id {config_id} not found'
            }, status=404)
    else:
        # 获取配置列表
        configs = CottonConfig.objects.all().order_by('-created_at')
        data = [{
            'id': config.id,
            'name': config.name,
            'created_at': config.created_at.isoformat(),
            'updated_at': config.updated_at.isoformat()
        } for config in configs]
        return JsonResponse({
            'success': True,
            'data': data,
            'count': len(data)
        }, safe=False)


def handle_post(request):
    """处理POST请求（创建新配置）"""
    try:
        data = json.loads(request.body)

        # 必填字段验证
        if not data.get('name'):
            raise ValidationError('Configuration name is required')

        # 创建配置
        config = CottonConfig.objects.create(
            name=data['name'],
            length_strength_params=data.get('length_strength_params', []),
            micronaire_params=data.get('micronaire_params', []),
            hand_machine_length_params=data.get('hand_machine_length_params', []),
            processing_quality_params=data.get('processing_quality_params', []),
            origin_params=data.get('origin_params', []),
            fiber_quality_params=data.get('fiber_quality_params', []),
            rejection_criteria=data.get('rejection_criteria', []),
            policy_params=data.get('policy_params', [])
        )

        return JsonResponse({
            'success': True,
            'message': 'Configuration created successfully',
            'id': config.id,
            'name': config.name
        }, status=201)

    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON format'
        }, status=400)
    except ValidationError as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Failed to create configuration: {str(e)}'
        }, status=500)


def handle_delete(request, config_id):
    """处理DELETE请求"""
    if not config_id:
        return JsonResponse({
            'success': False,
            'error': 'Configuration ID is required for deletion'
        }, status=400)

    try:
        config = CottonConfig.objects.get(id=config_id)
        config.delete()
        return JsonResponse({
            'success': True,
            'message': f'Configuration "{config.name}" deleted successfully'
        }, status=200)

    except CottonConfig.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': f'Configuration with id {config_id} not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Failed to delete configuration: {str(e)}'
        }, status=500)


# calculator/views.py
from .utils import parse_certificate
from .utils import execute_lua


class CertificateUploadView(APIView):
    def post(self, request):
        file = request.FILES.get('file')
        if not file:
            return Response({'error': '未上传文件'}, status=400)

        # 同步创建和处理证书
        cert = CottonCertificate.objects.create(
            file=file,
            original_name=file.name,
            status='processing'  # 直接标记为处理中
        )

        try:
            # 1. 解析证书（同步）
            input_data = parse_certificate(cert.file.path)

            # 2. 执行Lua计算（同步）
            lua_result = execute_lua(input_data)

            # 3. 存储结果（同步）
            CalculationResult.objects.create(
                certificate=cert,
                premium=lua_result['premium'],
                details=lua_result['details'],
                is_rejected=lua_result.get('is_rejected', False),
                rejection_reason=lua_result.get('rejection_reason', '')
            )
            cert.status = 'completed'
        except Exception as e:
            cert.status = 'failed'
            cert.error_message = str(e)
        finally:
            cert.save()

        return Response(
            CertificateUploadSerializer(cert).data,
            status=201
        )