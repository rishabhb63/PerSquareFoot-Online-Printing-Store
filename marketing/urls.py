from django.urls import path, re_path
from . import views

urlpatterns = [
    path("ajax/email_signup/", views.email_signup, name="ajax_email_signup"),

]