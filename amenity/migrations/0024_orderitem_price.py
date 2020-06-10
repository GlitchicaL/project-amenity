# Generated by Django 3.0.4 on 2020-06-09 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('amenity', '0023_cart_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=7),
        ),
    ]