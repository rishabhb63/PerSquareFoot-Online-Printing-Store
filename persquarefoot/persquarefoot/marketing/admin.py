from django.contrib import admin
from .models import EmailMarketingSignUp


# Register your models here.
class EmailMarketingSignUpAdmin(admin.ModelAdmin):
    list_display = ['email', 'timestamp',]

    class Meta:
        model = EmailMarketingSignUp


admin.site.register(EmailMarketingSignUp, EmailMarketingSignUpAdmin)