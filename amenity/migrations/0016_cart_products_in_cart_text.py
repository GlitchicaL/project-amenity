# Generated by Django 3.0.4 on 2020-04-13 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('amenity', '0015_item'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='products_in_cart_text',
            field=models.TextField(default=''),
        ),
    ]
