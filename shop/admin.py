from django.contrib import admin
from .models import Product, Contact, Variation, newsletter
# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    search_fields = ['product_name', 'category', 'subcategory']
    list_display = ['category', 'subcategory', 'product_name', 'price']
    list_editable = ['product_name', 'price']
    list_filter = ['category']
    prepopulated_fields = {'slug': ('product_name',)}

    class Meta:
        model = Product


class newsletterAdmin(admin.ModelAdmin):
    search_fields = ['name', 'email']
    list_display = ['newsletter_id', 'name', 'email', 'timestamp','daily']

    class Meta:
        model = newsletter
        fields = ["text", "daily"]
        labels = {"text": "", "daily": "daily_newsletter"}


admin.site.register(Product, ProductAdmin)
admin.site.register(Contact)
admin.site.register(Variation)
admin.site.register(newsletter, newsletterAdmin)
