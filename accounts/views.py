import re
from django.shortcuts import render, HttpResponseRedirect, Http404
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
from django.urls import reverse

from .forms import LoginForm, RegistrationForm
from .models import EmailConfirmed
# Create your views here.


def logout_view(request):
    logout(request)
    messages.success(request, "Successfully logged out. Feel free to <a href='%s'>login</a> again !" %(reverse("auth_login")), extra_tags='safe')
    return HttpResponseRedirect('%s'%(reverse("auth_login")))


def login_view(request):
    form = LoginForm(request.POST or None)
    btn = "Login"
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        login(request, user)
        messages.success(request, "Successfully logged in. Welcome back %s !" %(user.username))
        return HttpResponseRedirect("../../shop/")
    context = {
        "form": form,
        "submit_btn": btn,
    }
    return render(request, "form.html", context)


def registration_view(request):
    form = RegistrationForm(request.POST or None)
    btn = "Register"
    if form.is_valid():
        new_user = form.save(commit=False)
        #new_user.first_name = 'Rishabh'  this is where u can do stuff with model form
        new_user.save()
        messages.success(request, "Successfully Registered. Please confirm through your email.")
        return HttpResponseRedirect("../../shop/")
        # username = form.cleaned_data['username']
        # password = form.cleaned_data['password']
        # user = authenticate(username=username, password=password)
        # login(request, user)
    context = {
        "form": form,
        "submit_btn": btn,
    }
    return render(request, "form.html", context)


SHA1_RE = re.compile('^[a-f0-9]{40}$')


def activation_view(request, activation_key):
    if SHA1_RE.search(activation_key):
        try:
            instance = EmailConfirmed.objects.get(activation_key=activation_key)
        except EmailConfirmed.DoesNotExist:
            instance = None
            messages.error(request, "There was an error with your request.")
            return HttpResponseRedirect("../../shop/")
        if instance is not None and not instance.confirmed:
            page_message = "Confirmation Successful ! Welcome .."
            instance.confirmed = True
            instance.activation_key = "Confirmed"
            instance.save()
            messages.success(request, "Successfully Confirmed. Please login.")
        elif instance is not None and instance.confirmed:
            page_message = "Already Confirmed !"
            messages.success(request, "Already Confirmed.")
        else:
            pass
        context = {"page_message": page_message, }
        return render(request, "accounts/activation_complete.html", context)
    else:
        raise Http404
