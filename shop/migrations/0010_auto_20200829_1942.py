# Generated by Django 3.1 on 2020-08-29 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_auto_20200829_1923'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsletter',
            name='daily',
            field=models.BooleanField(default=True),
        ),
    ]
