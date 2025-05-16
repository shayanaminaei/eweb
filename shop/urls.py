from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('product/<slug:product_slug>/', views.product_detail, name='product_detail'),

    path('login/', auth_views.LoginView.as_view(template_name='shop/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('signup/', views.signup, name='signup'),

    path('cart/add/<slug:product_slug>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/remove/<slug:product_slug>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<slug:product_slug>/', views.update_cart_item, name='update_cart_item'),
]
