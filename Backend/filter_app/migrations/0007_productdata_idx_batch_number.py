# Generated by Django 5.1.6 on 2025-03-07 02:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('filter_app', '0006_remove_productdata_unique_batch_date_and_more'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='productdata',
            index=models.Index(fields=['batch_number'], name='idx_batch_number'),
        ),
    ]
