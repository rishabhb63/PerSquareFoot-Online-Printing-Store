# Generated by Django 3.1 on 2020-08-25 20:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_variations'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Variations',
            new_name='Variation',
        ),
    ]
