# Generated by Django 3.1 on 2020-08-23 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(default='', max_length=50)),
                ('subcategory', models.CharField(default='', max_length=50)),
                ('product_name', models.CharField(max_length=50)),
                ('desc', models.CharField(max_length=300)),
                ('description_1', models.TextField(blank=True)),
                ('description_2', models.TextField(blank=True)),
                ('description_3', models.TextField(blank=True)),
                ('price', models.DecimalField(decimal_places=2, default=39.99, max_digits=20)),
                ('thumbnail', models.ImageField(blank=True, upload_to='shop/images')),
                ('image1', models.ImageField(blank=True, upload_to='shop/images')),
                ('image2', models.ImageField(blank=True, upload_to='shop/images')),
                ('image3', models.ImageField(blank=True, upload_to='shop/images')),
                ('image4', models.ImageField(blank=True, upload_to='shop/images')),
                ('image5', models.ImageField(blank=True, upload_to='shop/images')),
                ('image6', models.ImageField(blank=True, upload_to='shop/images')),
                ('image7', models.ImageField(blank=True, upload_to='shop/images')),
                ('image8', models.ImageField(blank=True, upload_to='shop/images')),
            ],
        ),
    ]