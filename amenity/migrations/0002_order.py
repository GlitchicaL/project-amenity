# Generated by Django 3.0.4 on 2020-04-08 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('amenity', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.IntegerField(null=True, unique=True, verbose_name='Order ID')),
                ('products', models.ManyToManyField(to='amenity.Product')),
            ],
        ),
    ]
