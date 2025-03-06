from django.db import models

class Products(models.Model):
    product_name = models.CharField(max_length=50)

    def __str__(self):
        return self.product_name

class ProductData(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    batch_number = models.CharField(max_length=20)
    production_area = models.CharField(max_length=50)
    production_place = models.CharField(max_length=50)
    type = models.CharField(max_length=20)
    color_grade = models.CharField(max_length=20)
    length = models.DecimalField(max_digits=5, decimal_places=2)
    strength = models.DecimalField(max_digits=5, decimal_places=2)
    code_value = models.DecimalField(max_digits=5, decimal_places=2)
    moisture_regain = models.DecimalField(max_digits=5, decimal_places=2)
    impurity_content = models.DecimalField(max_digits=5, decimal_places=2)
    length_uniformity = models.DecimalField(max_digits=5, decimal_places=2)
    weight = models.DecimalField(max_digits=10, decimal_places=2)
    warehouse = models.CharField(max_length=50)
    quotation_method = models.CharField(max_length=20)
    outbound_basis = models.IntegerField()
    region = models.CharField(max_length=20)
    update_date = models.DateField()

    def __str__(self):
        return self.batch_number