from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="ShopHome"),
    path("productlist/", views.productlist, name="ProductList"),
    path("newsletter/", views.Newsletter, name="Newsletter"),
    path("about/", views.about, name="AboutUs"),
    path("contact/", views.contact, name="ContactUs"),
    path("tracker/", views.tracker, name="TrackingStatus"),
    path("search/", views.search, name="search"),
    path("products/<int:myid>", views.productView, name="ProductView"),
]