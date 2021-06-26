from django.contrib import messages
from django.http import HttpResponse
from shop.models import Product, Variation
from django.shortcuts import render,HttpResponseRedirect
from django.template.context_processors import request
from django.views.generic import TemplateView
from .models import Cart, CartItems
from django.urls import reverse

# Create your views here.


def view(request):
    try:
        the_id = request.session['cart_id']
        cart = Cart.objects.get(id=the_id)
    except:
        the_id = None
    if the_id:
        new_total = 0.00
        for item in cart.cartitems_set.all():
            line_total = float(item.product.price) * item.quantity
            new_total += line_total
        request.session['cart_items_total'] = cart.cartitems_set.count()
        cart.total = new_total
        cart.save()
        products = Product.objects.all()
        context = {
            "cart": cart,
            "products": products,
        }
    else:
        empty_message = "Your Cart is Empty, Please keep shopping..!"
        context = {"empty": True, "empty_message": empty_message}

    template = "cart/cartview.html"
    return render(request, template, context)


def remove_from_cart(request, id):
    try:
        the_id = request.session['cart_id']
        cart = Cart.objects.get(id=the_id)
    except:
        return HttpResponseRedirect(reverse("cart"))
    cartitem = CartItems.objects.get(id=id)
    cartitem.delete()
    messages.error(request, "Item removed from your cart. Keep Shopping..")
    return HttpResponseRedirect(reverse("cart"))


def add_to_cart(request, myid):
    request.session.set_expiry(120000)
    # check cart exist or not
    try:
        the_id = request.session['cart_id']
    except:
        # create new cart id
        new_cart = Cart()
        new_cart.save()
        request.session['cart_id'] = new_cart.id
        the_id = new_cart.id
    cart = Cart.objects.get(id=the_id)

    try:
        product = Product.objects.get(id=myid)
    except Product.DoesNotExists:
        pass
    except:
        pass
    product_var = [] # product variation list
    if request.method == "POST":
        qty = request.POST['qty']
        for item in request.POST:
            key = item
            val = request.POST[key]
            try:
                v = Variation.objects.get(product=product, category__iexact=key, title__iexact=val)
                product_var.append(v)
            except:
                pass
        cart_item = CartItems.objects.create(cart=cart, product=product)
        if len(product_var) > 0:
            cart_item.variations.add(*product_var)
        cart_item.quantity = qty
        cart_item.save()
        cart.save()
        return HttpResponseRedirect(reverse("cart"))
    return HttpResponseRedirect(reverse("cart"))
