from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('contact', views.contact, name='contact'),
    path('product', views.product, name='product'),
    path('product-details/<slug>', views.product_details, name='product-details'),
    path('add-to-cart/<product_id>', views.add_to_cart, name='add-to-cart'),
    path('cart-list', views.cart_list, name='cart-list'),
    path('increment-quantity/<cart_id>', views.increment_quantity, name='increment-quantity'),
    path('decrement-quantity/<cart_id>', views.decrement_quantity, name='decrement-quantity'),
    path('delete-quantity/<cart_id>', views.delete_quantity, name='delete-quantity'),
    path('clear-cart', views.clear_cart, name='clear-cart'),
    path('checkout', views.checkout, name='checkout'),
    path('search', views.search_product, name='search'),
    path('register', views.user_register, name='register'),
    path('login', views.user_login, name='login'),
    path('logout', views.user_logout, name='logout'),

]
