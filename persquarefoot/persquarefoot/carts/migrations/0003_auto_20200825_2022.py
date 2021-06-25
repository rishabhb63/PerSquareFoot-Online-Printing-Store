# Generated by Django 3.1 on 2020-08-25 14:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0002_auto_20200825_1950'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='items',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='products',
        ),
        migrations.AddField(
            model_name='cartitems',
            name='cart',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='carts.cart'),
        ),
        migrations.AddField(
            model_name='cartitems',
            name='line_total',
            field=models.DecimalField(decimal_places=2, default=10.99, max_digits=1000),
        ),
    ]
