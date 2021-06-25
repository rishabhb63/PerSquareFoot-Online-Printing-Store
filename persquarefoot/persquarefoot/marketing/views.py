import json
from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.http import HttpResponseBadRequest
from .forms import EmailForm
from .models import EmailMarketingSignUp


# Create your views here.
def email_signup(request):
    if request.method == "POST":
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            new_signup = EmailMarketingSignUp.objects.create(email=email)
            request.session['email_added_marketing'] = True
            return HttpResponse('Success %s' %(email))
        if form.errors:
            json_data = json.dumps(form.errors)
            return HttpResponseBadRequest(json_data, content_type='application/json')
    else:
        raise Http404