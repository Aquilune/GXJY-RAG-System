from django.db import models
from django.db.models import UniqueConstraint


class ProductData(models.Model):
    batch_number = models.CharField(max_length=20)
    production_area = models.CharField(max_length=50)
    production_place = models.CharField(max_length=50)
    type = models.CharField(max_length=20)
    color_grade = models.CharField(max_length=50)
    length = models.DecimalField(max_digits=5, decimal_places=2)
    strength = models.DecimalField(max_digits=5, decimal_places=2)
    code_value = models.DecimalField(max_digits=5, decimal_places=2)
    moisture_regain = models.DecimalField(max_digits=5, decimal_places=2)
    impurity_content = models.DecimalField(max_digits=5, decimal_places=2)
    length_uniformity = models.DecimalField(max_digits=5, decimal_places=2)
    weight = models.DecimalField(max_digits=10, decimal_places=2)
    warehouse = models.CharField(max_length=50, null=True, blank=True)
    quotation_method = models.CharField(max_length=20)
    quotation_method2 = models.CharField(max_length=20)
    quotation_method3 = models.CharField(max_length=20, null=True, blank=True)
    bid = models.DecimalField(max_digits=10, decimal_places=2)
    settlement = models.CharField(max_length=20)
    freight = models.CharField(max_length=50)
    outbound_basis = models.IntegerField(null=True, blank=True)
    update_date = models.DateField()

    def __str__(self):
        return self.batch_number

    class Meta:
        constraints = [
            UniqueConstraint(fields=['batch_number', 'update_date', 'quotation_method'], name='unique_batch_date_quatation')
        ]
        indexes = [
            models.Index(fields=['batch_number'], name='idx_batch_number'),
        ]