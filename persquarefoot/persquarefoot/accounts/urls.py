from django.urls import path, re_path
from . import views

urlpatterns = [
    path("logout/", views.logout_view, name="auth_logout"),
    path("login/", views.login_view, name="auth_login"),
    path("register/", views.registration_view, name="auth_registration"),
    re_path(r'^activate/(?P<activation_key>\w+)/$', views.activation_view, name="activation_view"),


]