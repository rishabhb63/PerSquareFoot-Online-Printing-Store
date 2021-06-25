from decimal import Decimal
from django.conf import settings
from django.db import models
from carts.models import Cart
# Create your models here.

STATUS_CHOICES = (
    ("Started", "Started"),
    ("Abandoned", "Abandoned"),
    ("Finished", "Finished"),
)

try:
    tax_rate = settings.DEFAULT_TAX_RATE
except Exception as e:
    print(str(e))
    raise NotImplementedError(str(e))


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, on_delete=models.CASCADE, null=True)
    order_id = models.CharField(max_length=120, default='ABC')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    status = models.CharField(max_length=120, choices=STATUS_CHOICES, default="Started")
    shipping_address = models.ForeignKey('UserAddress', related_name='shipping_address',\
                                         on_delete=models.CASCADE, null=True, blank=True)
    billing_address = models.ForeignKey('UserAddress', related_name='billing_address',\
                                        on_delete=models.CASCADE, null=True, blank=True)
    sub_total = models.DecimalField(default=10.99, max_digits=1000, decimal_places=2)
    tax_total = models.DecimalField(default=0.00, max_digits=1000, decimal_places=2)
    final_total = models.DecimalField(default=10.99, max_digits=1000, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.order_id

    def get_final_amount(self):
        instance = Order.objects.get(id=self.id)
        two_places = Decimal(10) ** -2
        tax_rate_dec = Decimal("%s" %(tax_rate))
        sub_total_dec = Decimal(self.sub_total)
        tax_total_dec = Decimal(tax_rate_dec * sub_total_dec).quantize(two_places)
        instance.tax_total = tax_total_dec
        instance.final_total = sub_total_dec + tax_total_dec
        instance.save()
        return self.final_total


class UserDefaultAddress(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    shipping = models.ForeignKey("UserAddress", null=True, blank=True,\
                                 on_delete=models.CASCADE, related_name="user_address_shipping_default")
    billing = models.ForeignKey("UserAddress", null=True, blank=True,\
                                on_delete=models.CASCADE, related_name="user_address_billing_default")

    def __str__(self):
        return str(self.user.username)


class UserAddressManager(models.Manager):

    def get_billing_addresses(self, user):
        return super(UserAddressManager, self).filter(billing=True).filter(user=user)

    def get_shipping_addresses(self, user):
        return super(UserAddressManager, self).filter(shipping=True).filter(user=user)


class UserAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    address = models.CharField(max_length=120)
    address2 = models.CharField(max_length=120, null=True, blank=True)
    city = models.CharField(max_length=120)
    state = models.CharField(max_length=120, null=True, blank=True)
    country = models.CharField(max_length=120)
    zipcode = models.CharField(max_length=25)
    phone = models.CharField(max_length=120)
    shipping = models.BooleanField(default=True)
    billing = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.get_address()

    def get_address(self):
        return "%s, %s, %s, %s, %s" % (self.address, self.city, self.state, self.country, self.zipcode)

    objects = UserAddressManager()

    class Meta:
        ordering = ['-updated', '-timestamp']
