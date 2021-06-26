from django.urls import path
from . import views

urlpatterns = [
    path("shop/checkout/", views.checkout, name="checkout"),
    path("shop/orders/", views.orders, name="user_orders"),
    path("ajax/add_user_address/", views.add_user_address, name="ajax_add_user_address"),
    path("shop/address/add/", views.add_user_address, name="add_user_address"),

]