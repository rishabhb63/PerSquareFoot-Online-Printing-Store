import stripe
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from carts.models import Cart
from .models import Order
from .forms import UserAddressForm
from .models import UserAddress, UserDefaultAddress
from django.conf import settings
from django.urls import reverse
from .utils import id_generator
from django.contrib import messages

stripe.api_key = "sk_test_51HNKmgEBQVudGdFBgF6gIgI23sgcLraKxYotME4sVN7q9xrVGZQD9Sj1SHq1NPhTAv8t490EwG6WbNLnXjTKfj6M00LsV2cx8c"


# Create your views here.
def orders(request):
    context = {}
    template = 'orders/user.html'
    return render(request, template, context)


# recquire user login
@login_required
def checkout(request):
    try:
        the_id = request.session['cart_id']
        cart = Cart.objects.get(id=the_id)
    except:
        the_id = None
        return HttpResponseRedirect(reverse("cart"))
    try:
        new_order = Order.objects.get(cart=cart)
    except Order.DoesNotExist:
        new_order = Order()
        new_order.cart = cart
        new_order.user = request.user
        new_order.order_id = id_generator()
        new_order.save()
    except:
        new_order = None
        # work on some error msg
        return HttpResponseRedirect(reverse("cart"))
    final_amount = 0
    if new_order is not None:
        new_order.sub_total = cart.total
        new_order.save()
        final_amount = new_order.get_final_amount()
    try:
        address_added = request.GET.get("address_added")
    except:
        address_added = None
    if address_added is None:
        address_form = UserAddressForm()
    else:
        address_form = None
    current_addresses = UserAddress.objects.filter(user=request.user)
    billing_addresses = UserAddress.objects.get_billing_addresses(user=request.user)
    # assign address to user
    # run credit card
    if request.method == "POST":
        try:
            user_stripe = request.user.userstripe.stripe_id
            customer = stripe.Customer.retrieve(user_stripe)

        except:
            customer = None
            pass
        if customer is not None:
            billing_a = request.POST['billing_address']
            shipping_a = request.POST['shipping_address']
            token = request.POST.get('stripeToken')
            try:
                billing_addresses_instance = UserAddress.objects.get(id=billing_a)
            except:
                billing_addresses_instance = None

            try:
                shipping_addresses_instance = UserAddress.objects.get(id=shipping_a)
            except:
                shipping_addresses_instance = None

            card = stripe.Customer.create_source(customer.id, source=token,)
            card.address_city = billing_addresses_instance.city or None
            card.address_state = billing_addresses_instance.state or None
            card.address_country = billing_addresses_instance.country or None
            card.address_line1 = billing_addresses_instance.address or None
            card.address_line2 = billing_addresses_instance.address2 or None
            card.address_zip = billing_addresses_instance.zipcode or None
            card.save()

            charge = stripe.Charge.create(
                amount=int(final_amount * 100),
                currency="inr",
                source=card,
                customer=customer,
                description="Charge for %s" %(request.user.username),
            )
            print(card)
            print(charge)
            if charge["captured"]:
                new_order.status = 'Finished'
                new_order.shipping_address = shipping_addresses_instance
                new_order.billing_address = billing_addresses_instance
                new_order.save()
                del request.session['cart_id']
                del request.session['cart_items_total']
                messages.success(request, "Thank you..Your order has been completed !")
                return HttpResponseRedirect(reverse("user_orders"))

    context = {
        "order": new_order,
        "address_form": address_form,
        "current_addresses": current_addresses,
        "billing_addresses": billing_addresses,
    }
    template = "shop/checkout.html"
    return render(request, template, context)


def add_user_address(request):
    try:
        next_page = request.GET.get("next")
    except:
        next_page = None
    form = UserAddressForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            new_address = form.save(commit=False)
            new_address.user = request.user
            new_address.save()
            is_default = form.cleaned_data["default"]
            if is_default:
                default_address, created = UserDefaultAddress.objects.get_or_create(user=request.user)
                is_shipping = form.cleaned_data["shipping"]
                if is_shipping:
                    default_address.shipping = new_address
                is_billing = form.cleaned_data["billing"]
                if is_billing:
                    default_address.billing = new_address
                default_address.save()

            if next_page is not None:
                return HttpResponseRedirect(reverse(str(next_page)))
    submit_btn = "Save Address"
    form_title = "Add new Address"
    return render(request, "form.html",
                  {"form": form,
                   "submit_btn": submit_btn,
                   "form_title": form_title,
                   })
