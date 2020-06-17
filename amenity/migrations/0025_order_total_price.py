# Generated by Django 3.0.4 on 2020-06-16 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('amenity', '0024_orderitem_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='total_price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=7),
        ),
    ]