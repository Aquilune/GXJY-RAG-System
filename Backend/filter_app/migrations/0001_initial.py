# Generated by Django 5.1.6 on 2025-03-06 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProductData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('batch_number', models.CharField(max_length=20)),
                ('production_area', models.CharField(max_length=50)),
                ('production_place', models.CharField(max_length=50)),
                ('type', models.CharField(max_length=20)),
                ('color_grade', models.CharField(max_length=20)),
                ('length', models.DecimalField(decimal_places=2, max_digits=5)),
                ('strength', models.DecimalField(decimal_places=2, max_digits=5)),
                ('code_value', models.DecimalField(decimal_places=2, max_digits=5)),
                ('moisture_regain', models.DecimalField(decimal_places=2, max_digits=5)),
                ('impurity_content', models.DecimalField(decimal_places=2, max_digits=5)),
                ('length_uniformity', models.DecimalField(decimal_places=2, max_digits=5)),
                ('weight', models.DecimalField(decimal_places=2, max_digits=10)),
                ('warehouse', models.CharField(max_length=50)),
                ('quotation_method', models.CharField(max_length=20)),
                ('quotation_method2', models.CharField(max_length=20)),
                ('quotation_method3', models.CharField(blank=True, max_length=20, null=True)),
                ('bid', models.DecimalField(decimal_places=2, max_digits=5)),
                ('settlement', models.CharField(max_length=20)),
                ('freight', models.CharField(max_length=50)),
                ('outbound_basis', models.IntegerField(blank=True, null=True)),
                ('update_date', models.DateField()),
            ],
        ),
    ]
