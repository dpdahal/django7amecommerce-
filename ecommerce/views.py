from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib import messages
from django.db.models import Q
from .forms import BuyerForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate


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


def checkout(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        address = request.POST['address']
        phone = request.POST['phone']
        product_unique_cart_id = request.session.get('product_unique_cart_key')
        cat_obj = UniqueCart.objects.get(id=product_unique_cart_id)
        order_object = Order.objects.create(
            name=name, email=email, address=address, phone=phone, rate=cat_obj.total, sub_total=cat_obj.total,
            cart=UniqueCart.objects.get(id=cat_obj.id)
        )
        order_object.save()
        del request.session['product_unique_cart_key']
        return redirect('index')

    else:
        product_unique_cart_id = request.session.get('product_unique_cart_key')
        if product_unique_cart_id:
            data = UniqueCart.objects.get(id=product_unique_cart_id)
            content = {
                'allCartData': data
            }
            return render(request, 'pages/product/checkout.html', content)
        else:
            return redirect('index')


def product(request):
    content = {
        'productData': Product.objects.all()
    }
    return render(request, 'pages/product/product.html', content)


def search_product(request):
    if request.GET['q'] == "":
        return redirect('index')
    else:
        criteria = request.GET['q']
        criteria = str(criteria).lower()
        p_data = Product.objects.filter(Q(product_name__icontains=criteria) | Q(category_id__category_name=criteria))
        content = {
            'productData': p_data,
            'criteria': criteria
        }
        return render(request, 'pages/product/product.html', content)


def user_register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        full_name = request.POST['full_name']
        address = request.POST['address']
        phone = request.POST['phone']
        user_data = User.objects.create(username=username, email=email, password=password)
        Buyer.objects.create(user_id=user_data.id, full_name=full_name, address=address, phone=phone)
        login(request, user_data)
        return redirect('index')
    else:
        content = {
            'buyerForm': BuyerForm()
        }
        return render(request, 'pages/users/register.html', content)


def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user_data = authenticate(username=username, password=password)
        if user_data:
            login(request, user_data)
            return redirect('index')
        else:
            return redirect(request.META.get('HTTP_REFERER'))

    else:
        return render(request, 'pages/users/login.html')


def user_logout(request):
    logout(request)
    return redirect('index')
