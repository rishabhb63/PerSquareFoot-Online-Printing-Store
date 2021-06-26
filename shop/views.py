from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from .models import Product, Contact, newsletter
from math import ceil


# Create your views here.
def index(request):
    products = Product.objects.all()
    # print(products)
    # n = len(products)
    # nSlides = n//4 + ceil((n/4)-(n//4))

    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])

    # params = {'no_of_slides':nSlides, 'range': range(1,nSlides),'product': products}
    # allProds = [[products, range(1, nSlides), nSlides],
    #             [products, range(1, nSlides), nSlides]]
    params = {'products': products, 'allProds': allProds}
    return render(request, 'shop/index.html', params)


def about(request):
    products = Product.objects.all()
    params = {'product': products}
    return render(request, 'shop/about.html', params)


def productlist(request):
    product1 = Product.objects.filter(category="Outdoor Signage")
    product2 = Product.objects.filter(category="Indoor Signage")
    product3 = Product.objects.filter(category="Other Services")
    product4 = Product.objects.filter(category="Promotional items")
    product5 = Product.objects.filter(category="Alphabet Cutting")
    params = {'product1': product1,
              'product2': product2,
              'product3': product3,
              'product4': product4,
              'product5': product5,
              }
    return render(request, 'shop/ProductList.html', params)


def contact(request):
    if request.method == "POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        whatsapp = request.POST.get('whatsapp', '')
        desc = request.POST.get('desc', '')
        contact = Contact(name=name, email=email, phone=phone, whatsapp=whatsapp, desc=desc)
        contact.save()
        return HttpResponseRedirect('../')
    return render(request, 'shop/contact.html')


def tracker(request):
    return HttpResponse("We are at Tracker")


def search(request):
    try:
        keywords = request.GET.get('keywords')
    except:
        field_keywords = None
    if keywords:
        products = Product.objects.filter(product_name__icontains=keywords)
        context = {'query': keywords, 'products': products}
        template = 'shop/results.html'
    else:
        template = 'shop/index.html'
        context = {}
    return render(request, template, context)


def productView(request, myid):
    # Fetch the product using the id
    product = Product.objects.filter(id=myid)
    return render(request, 'shop/prodView.html', {'product': product[0]})


def Newsletter(request):
    if request.method == "POST":
        myname = request.POST.get('myname', '')
        myemail = request.POST.get('myemail', '')
        daily = request.POST.get('daily', '')
        if daily == 'on':
            daily = True
        else:
            daily = False
        newsletters = newsletter(name=myname, email=myemail, daily=daily)
        newsletters.save()
    return HttpResponseRedirect(reverse('ShopHome'))

