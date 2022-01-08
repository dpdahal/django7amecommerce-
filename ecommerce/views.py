from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib import messages


# Create your views here.

def index(request):
    return render(request, 'pages/home/home.html')


def contact(request):
    content = {
        'title': "Contact Us"
    }
    return render(request, 'pages/contact/contact.html', content)


def product_details(request, slug):
    get_product = Product.objects.get(product_slug=slug)
    cat_id = get_product.category_id.id
    rr_product = Product.objects.filter(category_id=cat_id)
    content = {
        'title': get_product.product_name,
        'productData': get_product,
        'relatedProduct': rr_product
    }
    return render(request, 'pages/product/product-details.html', content)


def add_to_cart(request, product_id):
    p_id = product_id
    find_product_object = Product.objects.get(id=p_id)
    product_session_key = request.session.get('product_unique_cart_key', None)
    if product_session_key:
        cart_object = UniqueCart.objects.get(id=product_session_key)
        exists_product = cart_object.cartproduct_set.filter(product=find_product_object)
        if exists_product:
            product_object = exists_product.last()
            product_object.quantity += 1
            product_object.sub_total += find_product_object.s_price
            product_object.save()
            cart_object.total += find_product_object.s_price
            cart_object.save()
        else:
            cart_product = CartProduct.objects.create(
                cart=cart_object,
                product=find_product_object,
                rate=find_product_object.s_price,
                quantity=1,
                sub_total=find_product_object.s_price

            )
            cart_product.save()
            cart_object.total += find_product_object.s_price
            cart_object.save()

    else:
        unique_cart_object = UniqueCart.objects.create(total=0)
        request.session['product_unique_cart_key'] = unique_cart_object.id
        cart_product = CartProduct.objects.create(
            cart=unique_cart_object,
            product=find_product_object,
            rate=find_product_object.s_price,
            quantity=1,
            sub_total=find_product_object.s_price
        )
        cart_product.save()
        unique_cart_object.total += find_product_object.s_price
        unique_cart_object.save()

    messages.success(request, "Cart was successfully create")
    return redirect(request.META.get('HTTP_REFERER'))


def cart_list(request):
    product_unique_cart_id = request.session.get('product_unique_cart_key')
    if product_unique_cart_id:
        data = UniqueCart.objects.get(id=product_unique_cart_id)
    else:
        data = None

    content = {
        'allCartData': data
    }

    return render(request, 'pages/product/cat-list.html', content)


def increment_quantity(request, cart_id):
    get_cat_id = cart_id
    cart_product_object = CartProduct.objects.get(id=get_cat_id)
    ct = cart_product_object.cart
    cart_product_object.quantity += 1
    cart_product_object.sub_total += cart_product_object.rate
    cart_product_object.save()
    ct.total += cart_product_object.rate
    ct.save()
    messages.success(request, "Cart was successfully update")
    return redirect(request.META.get('HTTP_REFERER'))


def decrement_quantity(request, cart_id):
    get_cat_id = cart_id
    cart_product_object = CartProduct.objects.get(id=get_cat_id)
    ct = cart_product_object.cart
    cart_product_object.quantity -= 1
    cart_product_object.sub_total -= cart_product_object.rate
    cart_product_object.save()
    ct.total -= cart_product_object.rate
    ct.save()
    if cart_product_object.quantity == 0:
        cart_product_object.delete()
    messages.success(request, "Cart was successfully update")
    return redirect(request.META.get('HTTP_REFERER'))


def delete_quantity(request, cart_id):
    get_cat_id = cart_id
    cart_product_object = CartProduct.objects.get(id=get_cat_id)
    ct = cart_product_object.cart
    ct.total -= cart_product_object.sub_total
    ct.save()
    cart_product_object.delete()
    messages.success(request, "Cart was successfully deleted")
    return redirect(request.META.get('HTTP_REFERER'))


def clear_cart(request):
    get_key = request.session.get('product_unique_cart_key')
    cart = UniqueCart.objects.get(id=get_key)
    cart.cartproduct_set.all().delete()
    cart.total = 0
    cart.save()
    messages.success(request, "Cart was successfully remove")
    return redirect(request.META.get('HTTP_REFERER'))
