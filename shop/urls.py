from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView
from . import views

urlpatterns = [
    path("", views.index, name="ShopHome"),
    path("about/", views.about, name="AboutUs"),
    path("contact/", views.contact, name="ContactUs"),
    path("tracker/", views.tracker, name="TrackingStatus"),
    path("search/", views.search, name="Search"),
    path("products/<int:myid>", views.products, name="Products"),
    path('allproducts/',views.allproducts,name='Allproducts'),
    path("checkout/", views.checkout, name="Checkout"),
    path('cart/', views.cart, name='cart'),
    path('favorites/', views.favorites, name='favorites'),
    path('userorders/', views.user_orders, name='user_orders'),

    path('favorites_storage/', views.favorites_storage, name='favorites_storage'),
    path('register/', views.register, name='register_view'),
     path('login/',views.login,  name='login'),
     path('logout/', views.user_logout, name='logout'),
   
]   
