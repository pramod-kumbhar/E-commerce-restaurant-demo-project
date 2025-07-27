from django.urls import path
from . import views

app_name = "hotelapp"

urlpatterns = [
    path('home/', views.home, name='home'),
    path('home/booking', views.booking, name='booking'),
    path('menu/', views.menu, name='menu'),
    path("add_to_cart/<int:product_id>/",views.add_to_cart, name='add_to_cart'),
    path("cart/",views.view_cart, name='view_cart'),
    path("order/",views.order_detail, name='order_detail'),
    path("place_order/", views.place_order, name="place_order"),
]
