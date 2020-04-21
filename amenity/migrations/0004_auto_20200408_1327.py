# Generated by Django 3.0.4 on 2020-04-08 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('amenity', '0003_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('OR', 'Ordered'), ('SH', 'Shipped'), ('DE', 'Delivered')], default='Ordered', max_length=2),
        ),
    ]
