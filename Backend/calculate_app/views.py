import json
from pathlib import Path

from django.core.paginator import Paginator, EmptyPage
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CottonConfig, CalculationResult
from .serializers import CottonConfigSerializer
from .utils import process_excel_with_lua


class BaseAPIView(APIView):
    """所有API视图的基类，提供统一错误处理"""

    def handle_exception(self, exc):
        if isinstance(exc, ValidationError):
            return Response(
                {'success': False, 'error': str(exc)},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().handle_exception(exc)

class CottonConfigAPI(BaseAPIView):
    """配置管理统一接口"""

    def get(self, request, config_id=None):
        if config_id:
            # 获取单个配置详情
            try:
                config = CottonConfig.objects.get(id=config_id)
                serializer = CottonConfigSerializer(config)
                return Response({
                    'success': True,
                    'data': serializer.data
                })
            except CottonConfig.DoesNotExist:
                return Response({
                    'success': False,
                    'error': '配置不存在'
                }, status=status.HTTP_404_NOT_FOUND)
        else:
            # 获取配置列表
            configs = CottonConfig.objects.all().order_by('-created_at')
            serializer = CottonConfigSerializer(configs, many=True)
            return Response({
                'success': True,
                'data': serializer.data,
                'count': len(serializer.data)
            })

    def post(self, request):
        """创建新配置"""
        serializer = CottonConfigSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'success': False,
            'error': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, config_id):
        """删除配置"""
        try:
            config = CottonConfig.objects.get(id=config_id)
            config.delete()
            return Response({
                'success': True,
                'message': '配置已删除'
            })
        except CottonConfig.DoesNotExist:
            return Response({
                'success': False,
                'error': '配置不存在'
            }, status=status.HTTP_404_NOT_FOUND)


from .models import CottonCertificate
from .serializers import CertificateSerializer


class CertificateAPI(BaseAPIView):
    """证书管理统一接口"""

    def get(self, request, cert_id=None):
        if cert_id:
            # 获取证书详情
            try:
                cert = CottonCertificate.objects.get(id=cert_id)
                serializer = CertificateSerializer(cert)
                return Response({
                    'success': True,
                    'data': serializer.data
                })
            except CottonCertificate.DoesNotExist:
                return Response({
                    'success': False,
                    'error': '证书不存在'
                }, status=status.HTTP_404_NOT_FOUND)
        else:
            # 分页查询证书列表
            page = request.query_params.get('page', 1)
            page_size = request.query_params.get('page_size', 10)

            queryset = CottonCertificate.objects.all().order_by('-created_at')
            paginator = Paginator(queryset, page_size)

            try:
                certs = paginator.page(page)
                serializer = CertificateSerializer(certs, many=True)
                return Response({
                    'success': True,
                    'data': serializer.data,
                    'total': paginator.count,
                    'page': int(page)
                })
            except EmptyPage:
                return Response({
                    'success': False,
                    'error': '页码超出范围'
                }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, cert_id):
        """删除证书"""
        try:
            cert = CottonCertificate.objects.get(id=cert_id)
            cert.delete()
            return Response({
                'success': True,
                'message': '证书已删除'
            })
        except CottonCertificate.DoesNotExist:
            return Response({
                'success': False,
                'error': '证书不存在'
            }, status=status.HTTP_404_NOT_FOUND)


from django.core.files.storage import default_storage
from tempfile import NamedTemporaryFile
import os


class CertificateUploadAPI(BaseAPIView):
    def post(self, request):
        # 1. 验证文件上传
        if 'file' not in request.FILES:
            raise ValidationError('请选择要上传的Excel文件')

        file = request.FILES['file']

        # 2. 验证文件扩展名
        if not file.name.lower().endswith(('.xlsx', '.xls')):
            raise ValidationError('仅支持.xlsx或.xls格式的Excel文件')

        # 3. 创建临时存储
        try:
            with NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp_file:
                for chunk in file.chunks():
                    tmp_file.write(chunk)
                temp_path = tmp_file.name

            # 4. 执行Excel处理和Lua计算
            try:
                script_dir = Path(__file__).parent.absolute()
                lua_path = script_dir / 'calculator.lua'
                result = process_excel_with_lua(temp_path, lua_path)

                # 5. 保存结果到数据库
                cert = CottonCertificate.objects.create(
                    file=file,
                    original_name=file.name,
                    status='completed'
                )

                CalculationResult.objects.create(
                    certificate=cert,
                    premium=result['premium'],
                    details=json.dumps(result['details']),
                    is_rejected=result['is_rejected'],
                    rejection_reason=result['rejection_reason']
                )

                return Response({
                    'success': True,
                    'data': {
                        'certificate_id': cert.id,
                        'premium': result['premium'],
                        'is_rejected': result['is_rejected'],
                        'rejection_reason': result['rejection_reason']
                    }
                }, status=status.HTTP_201_CREATED)

            except ValueError as e:
                raise ValidationError(str(e))
            except Exception as e:
                raise RuntimeError(f"计算过程出错: {str(e)}")

        finally:
            # 6. 清理临时文件
            if 'temp_path' in locals() and os.path.exists(temp_path):
                os.unlink(temp_path)