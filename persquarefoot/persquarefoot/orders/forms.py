from .models import UserAddress
from django import forms


class UserAddressForm(forms.ModelForm):
    default = forms.BooleanField(label='Make Default', required=False)

    class Meta:
        model = UserAddress
        fields = ["address", "address2", "city", "state", "country", "zipcode", "phone", "shipping", "billing",]