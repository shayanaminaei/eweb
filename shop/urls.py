from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),  # صفحه اصلی محصولات
    path('signup/', views.signup, name='signup'),  # ثبت نام
    path('login/', auth_views.LoginView.as_view(template_name='shop/login.html'), name='login'),  # ورود
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),  # خروج

    path('products/', views.product_list, name='product_list'),  # لیست محصولات (اختیاری، چون home هم لیست داره)
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),  # جزئیات محصول

    path('cart/', views.cart_detail, name='cart_detail'),  # سبد خرید
    path('cart/add/<slug:product_slug>/', views.add_to_cart, name='add_to_cart'),  # افزودن به سبد خرید
    path('cart/remove/<slug:product_slug>/', views.remove_from_cart, name='remove_from_cart'),  # حذف از سبد خرید
    path('cart/update/<slug:product_slug>/', views.update_cart_item, name='update_cart_item'),  # بروزرسانی تعداد

]
