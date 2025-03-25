from django.db import models
from django.db.models import UniqueConstraint
from django.dispatch import receiver
from django.db.models.signals import pre_save

from filter_app.configurations import XINJIANG_WAREHOUSES


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
    warehouse_area = models.CharField(max_length=50, null=False, default='内地')
    batch_product_area = models.CharField(max_length=50, null=False, default='新疆')
    batch_product_year = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.batch_number

    class Meta:
        constraints = [
            UniqueConstraint(fields=['batch_number', 'update_date', 'quotation_method'], name='unique_batch_date_quatation')
        ]
        indexes = [
            models.Index(fields=['batch_number'], name='idx_batch_number'),
            models.Index(fields=['update_date'], name='idx_update_date')
        ]



@receiver(pre_save, sender=ProductData)
def update_warehouse_area(sender, instance, **kwargs):
    if instance.warehouse in XINJIANG_WAREHOUSES:
        instance.warehouse_area = '新疆'
    else:
        instance.warehouse_area = '内地'


@receiver(pre_save, sender=ProductData)
def update_batch_product_area(sender, instance, **kwargs):
    if instance.batch_number and len(instance.batch_number) >= 2 and instance.batch_number[:2] in ['65', '66']:
        instance.batch_product_area = '新疆'
    else:
        instance.batch_product_area = '地产'


@receiver(pre_save, sender=ProductData)
def update_batch_product_year(sender, instance, **kwargs):
    if instance.batch_number and len(instance.batch_number) >= 7:
        year_str = instance.batch_number[5:7]
        try:
            full_year = 2000 + int(year_str)
            instance.batch_product_year = full_year
        except ValueError:
            instance.batch_product_year = None