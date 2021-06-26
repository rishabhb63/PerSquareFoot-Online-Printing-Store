from django.db import models
from django.urls import reverse
# Create your models here.


class Product(models.Model):
    product_id = models.AutoField
    category=models.CharField(max_length=50, default="")
    subcategory = models.CharField(max_length=50, default="")
    product_name = models.CharField(max_length=50)
    desc = models.CharField(max_length=300)
    description_1 = models.TextField(blank=True)
    description_2 = models.TextField(blank=True)
    description_3 = models.TextField(blank=True)
    slug = models.SlugField(unique=True)
    price = models.DecimalField(decimal_places=2, max_digits=20, default=39.99)
    thumbnail = models.ImageField(upload_to="shop/images", blank=True)
    image1 = models.ImageField(upload_to="shop/images", blank=True)
    image2 = models.ImageField(upload_to="shop/images", blank=True)
    image3 = models.ImageField(upload_to="shop/images", blank=True)
    image4 = models.ImageField(upload_to="shop/images", blank=True)
    image5 = models.ImageField(upload_to="shop/images", blank=True)
    image6 = models.ImageField(upload_to="shop/images", blank=True)
    image7 = models.ImageField(upload_to="shop/images", blank=True)
    image8 = models.ImageField(upload_to="shop/images", blank=True)

    def __str__(self):
        return self.product_name
    class Meta:
        unique_together = ('product_name', 'slug')

    def get_absolute_url(self):
        return reverse("ProductView", kwargs={"myid": self.id})


class Contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=70, default="")
    phone = models.CharField(max_length=70, default="")
    whatsapp = models.CharField(max_length=70, default="")
    desc = models.CharField(max_length=500, default="")

    def __str__(self):
        return self.name


class VariationManager(models.Manager):
    def all(self):
        return super(VariationManager, self).filter(active=True)

    def sizes(self):
        return self.all().filter(category='size')

    def Select_Option(self):
        return self.all().filter(category='Select_Option')

    def Two_Sided(self):
        return self.all().filter(category='Two_Sided')

    def Premium(self):
        return self.all().filter(category='Premium')

    def Hanging_Options(self):
        return self.all().filter(category='Hanging_Options')

    def Lamination(self):
        return self.all().filter(category='Lamination')

    def Wind_Flaps(self):
        return self.all().filter(category='Wind_Flaps')

    def Accessories(self):
        return self.all().filter(category='Accessories')


VAR_CATEGORIES =(
    ('size', 'size'),
    ('Select_Option', 'Select_Option'),
    ('Two_Sided', 'Two_Sided'),
    ('Premium', 'Premium'),
    ('Hanging_Options', 'Hanging_Options'),
    ('Lamination', 'Lamination'),
    ('Wind_Flaps', 'Wind_Flaps'),
    ('Accessories', 'Accessories'),

)


class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    category = models.CharField(max_length=120, choices=VAR_CATEGORIES, default='size')
    title = models.CharField(max_length=120)
    image = models.ImageField(upload_to="shop/images", blank=True)
    price = models.DecimalField(max_digits=100,  decimal_places=2, null=True, blank=True)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    active = models.BooleanField(default=True)

    objects = VariationManager()

    def __str__(self):
        return self.title


class newsletter(models.Model):
    newsletter_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=70, default="")
    timestamp = models.DateTimeField(auto_now_add=True)
    daily = models.BooleanField(default=True)

    def __str__(self):
        return self.name
