# Generated by Django 3.0.4 on 2020-05-19 23:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('amenity', '0021_auto_20200519_1501'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='products_in_cart_text',
        ),
        migrations.RemoveField(
            model_name='order',
            name='products',
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='amenity.Order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='amenity.Product')),
            ],
        ),
    ]