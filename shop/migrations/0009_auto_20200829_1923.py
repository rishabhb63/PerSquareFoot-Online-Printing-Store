# Generated by Django 3.1 on 2020-08-29 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_newsletter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsletter',
            name='daily',
            field=models.BooleanField(),
        ),
    ]
