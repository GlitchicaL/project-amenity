# Generated by Django 3.0.4 on 2020-04-08 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('amenity', '0002_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('ordered', 'Ordered'), ('shipped', 'Shipped'), ('delivered', 'Delivered')], default='Ordered', max_length=50),
        ),
    ]