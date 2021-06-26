from django.urls import path, re_path
from . import views

urlpatterns = [
    path("", views.view, name="cart"),
    path("cart/cart/<int:id>/", views.remove_from_cart, name="remove_from_cart"),
    path("cart/<int:myid>/", views.add_to_cart, name="add_to_cart"),
    # re_path(r'^cart/(?P<myid>[0-9]+)/$',views.update_cart, name="update_cart"),
    # re_path(r'^bio/(?P<username>\w+)/$', views.bio, name='bio'),
    # path("cart/<int:myid>", views.update_cart, name="update_cart"),
    # path("hello", views.s, name="cart"),
]