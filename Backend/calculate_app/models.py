from django.db import models


class CottonConfig(models.Model):
    name = models.CharField(max_length=100, verbose_name="配置名称")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    # 长度/比强参数
    length_strength_params = models.JSONField(verbose_name="长度/比强参数")

    # 马克隆值参数
    micronaire_params = models.JSONField(verbose_name="马克隆值参数")

    # 手扯长度/机扯长度参数
    hand_machine_length_params = models.JSONField(verbose_name="手扯长度/机扯长度参数")

    # 轧工质量参数
    processing_quality_params = models.JSONField(verbose_name="轧工质量参数")

    # 产地参数
    origin_params = models.JSONField(verbose_name="产地参数")

    # 纤维品质参数
    fiber_quality_params = models.JSONField(verbose_name="纤维品质参数")

    # 拒收标准
    rejection_criteria = models.JSONField(verbose_name="拒收标准")

    # 政策性参数
    policy_params = models.JSONField(verbose_name="政策性参数")

    class Meta:
        verbose_name = "棉花参数配置"
        verbose_name_plural = "棉花参数配置"
        ordering = ['-created_at']

    def __str__(self):
        return self.name


from django.db import models
import uuid


class TimeStampedModel(models.Model):
    """时间戳抽象基类"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CottonCertificate(TimeStampedModel):
    """棉花检验证书"""
    STATUS_CHOICES = [
        ('pending', '待处理'),
        ('processing', '计算中'),
        ('completed', '已完成'),
        ('failed', '已失败')
    ]

    # 文件相关
    file = models.FileField(upload_to='certs/%Y/%m/')
    original_name = models.CharField(max_length=255)
    file_id = models.UUIDField(default=uuid.uuid4, unique=True)

    # 状态管理
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    error_message = models.TextField(blank=True)

    # 核心业务字段（自动解析填充）
    batch_number = models.CharField(max_length=50, blank=True)  # 批号
    warehouse = models.CharField(max_length=100, blank=True)  # 仓库
    origin = models.CharField(max_length=100, blank=True)  # 产地

    class Meta:
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['batch_number']),
        ]
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.batch_number or self.original_name} ({self.get_status_display()})"


class CalculationResult(TimeStampedModel):
    """计算结果存储"""
    certificate = models.OneToOneField(
        CottonCertificate,
        on_delete=models.CASCADE,
        related_name='result'
    )

    # 核心结果
    premium = models.DecimalField(max_digits=10, decimal_places=2)  # 升贴水值
    is_rejected = models.BooleanField(default=False)
    rejection_reason = models.CharField(max_length=200, blank=True)

    # 质量指标（解析证书后自动填充）
    color_grade = models.CharField(max_length=20, blank=True)  # 主体颜色级
    avg_length = models.FloatField(null=True)  # 平均长度(mm)
    avg_micronaire = models.FloatField(null=True)  # 平均马克隆值
    avg_strength = models.FloatField(null=True)  # 平均断裂比强度(cN/tex)

    # 详细数据（JSON存储完整计算结果）
    details = models.JSONField(default=dict)


class SystemConfig(models.Model):
    """系统参数配置"""
    PARAM_TYPES = [
        ('length', '长度参数'),
        ('strength', '比强参数'),
        ('micronaire', '马克隆值'),
        ('rejection', '拒收标准')
    ]

    param_type = models.CharField(max_length=20, choices=PARAM_TYPES, unique=True)
    values = models.JSONField()  # 存储对应类型的所有参数

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_param_type_display()}配置"