from rest_framework import serializers
from .models import CottonConfig, CottonCertificate, CalculationResult


class CottonConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = CottonConfig
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


class CalculationResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = CalculationResult
        fields = '__all__'


class CertificateSerializer(serializers.ModelSerializer):
    result = CalculationResultSerializer(source='calculation_result', read_only=True)

    class Meta:
        model = CottonCertificate
        fields = ['id', 'original_name', 'status', 'created_at', 'result']
        read_only_fields = ('status', 'created_at')