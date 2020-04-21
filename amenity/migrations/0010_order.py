# Generated by Django 3.0.4 on 2020-04-08 18:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20200407_1515'),
        ('amenity', '0009_delete_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.IntegerField(unique=True)),
                ('order_date', models.DateField(auto_now_add=True)),
                ('delivered_date', models.DateField(blank=True)),
                ('status', models.CharField(choices=[('OR', 'Ordered'), ('SH', 'Shipped'), ('DE', 'Delivered')], default='OR', max_length=2)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Customer')),
                ('products', models.ManyToManyField(to='amenity.Product')),
            ],
        ),
    ]
