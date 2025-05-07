from rest_framework import serializers
from .models import CottonConfig

class CottonConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = CottonConfig
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')



from rest_framework import serializers
from .models import CottonCertificate, CalculationResult

class CertificateUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = CottonCertificate
        fields = ['file_id', 'original_name', 'status', 'batch_number']
        read_only_fields = ['status']

class CalculationResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = CalculationResult
        fields = ['premium', 'is_rejected', 'rejection_reason', 'details']