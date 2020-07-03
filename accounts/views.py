from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.db import IntegrityError

from django.views.decorators.http import require_http_methods

from .models import Customer
from amenity.models import Product, Order, OrderItem, Cart, CartItem

import json

ERROR_MSGS = {
    '': '',
    'AC1': 'Passwords do not match.',
    'AC2': 'Username already exists!',
    'AL1': 'Incorrect username or password.',
}

#------------------------------------------------------------------------------------------------------------------------------#


def account(request, message=''):
    if request.user.is_authenticated:
        return redirect('account_dashboard')

    context = {
        'title': 'Register or Login',
        'message': ERROR_MSGS[message],
    }

    return render(request, 'accounts/account.html', context)

#------------------------------------------------------------------------------------------------------------------------------#


def create_account(request):
    if (request.method == 'POST'):
        # Obtain entered information
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']

        email = request.POST['email']
        username = request.POST['username']

        password = request.POST['password']
        password_retyped = request.POST['password_retyped']

        # Determine if both entered passwords match
        if (password != password_retyped):
            return redirect('login_page', message="AC1")

        # Create the user
        try:
            user = User.objects.create_user(username, email, password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
        except (IntegrityError):  # Exception raised if username already exists
            return redirect('login_page', message="AC2")

        # Assign user as a customer
        customer = Customer.objects.create(user=user)
        Cart.objects.create(customer=customer)

        # Login the user and redirect them to their dashboard
        login(request, user)
        return redirect('account_dashboard')
    else:
        return redirect('login_page')


#------------------------------------------------------------------------------------------------------------------------------#


def login_account(request):
    if (request.method == 'POST'):
        # Obtain entered information
        username = request.POST['username']
        password = request.POST['password']

        # Authenticate user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('account_dashboard')
        else:
            return redirect('login_page', message='AL1')


#------------------------------------------------------------------------------------------------------------------------------#


def logout_account(request):
    logout(request)
    return redirect('login_page')


#------------------------------------------------------------------------------------------------------------------------------#
# NOTE: Every function below this comment REQUIRES the user to be logged in!

@login_required(login_url='login_page')
def account_dashboard(request):
    user = User.objects.get(username=request.user)
    cart = Cart.objects.get(customer=user.customer)
    cart_items = CartItem.objects.filter(cart=cart)

    orders = Order.objects.filter(
        customer=user.customer).order_by('-order_date')[:3]

    products_in_cart = []
    price_of_cart = 0

    for item in cart_items:
        products_in_cart.append(item)
        price_of_cart += item.product.price * item.quantity

    context = {
        'title': 'Dashboard',
        'user': user,
        'orders': orders,
        'products_in_cart': products_in_cart,
        'price_of_cart': price_of_cart,
    }

    return render(request, 'accounts/account_dashboard.html', context)


#------------------------------------------------------------------------------------------------------------------------------#


@login_required(login_url='login_page')
def account_cart(request):
    cart = Cart.objects.get(customer=request.user.customer)
    cart_items = CartItem.objects.filter(cart=cart)

    products_in_cart = []
    price_of_cart = 0

    for item in cart_items:
        price_of_cart += item.product.price * item.quantity
        products_in_cart.append(item)

    cart.setPrice(price_of_cart)

    context = {
        'title': 'Cart',
        'products_in_cart': products_in_cart,
        'price_of_cart': cart.price,
    }

    return render(request, 'accounts/account_cart.html', context)


#------------------------------------------------------------------------------------------------------------------------------#


@require_http_methods(["POST"])
@login_required(login_url='login_page')
def account_edit_cart_quantity(request):
    data = json.loads(request.body)
    productId = data['productId']
    quantity = data['quantity']

    if (int(quantity) > 8):
        JsonTxt = 'Over Quantity Limit'
        return JsonResponse(JsonTxt, safe=False)

    cart = Cart.objects.get(customer=request.user.customer)
    cart_item = CartItem.objects.filter(
        cart=cart).get(product=productId)

    cart_item.quantity = quantity
    cart_item.save()

    JsonTxt = "Quantity Changed"
    return JsonResponse(JsonTxt, safe=False)


#------------------------------------------------------------------------------------------------------------------------------#


@require_http_methods(["POST"])
@login_required(login_url='login_page')
def account_remove_from_cart(request):
    data = json.loads(request.body)
    productId = data['productId']

    # Get the customer, and his/her cart
    cart = Cart.objects.get(customer=request.user.customer)
    cart_item = CartItem.objects.filter(
        cart=cart).filter(product=productId)

    cart_item.delete()

    JsonTxt = 'Item removed from cart!'
    return JsonResponse(JsonTxt, safe=False)


#------------------------------------------------------------------------------------------------------------------------------#


@login_required(login_url='login_page')
def account_empty_cart(request):
    cart = Cart.objects.get(customer=request.user.customer)
    cart_items = CartItem.objects.filter(cart=cart)

    cart_items.delete()

    return redirect('account_cart')


#------------------------------------------------------------------------------------------------------------------------------#


@login_required(login_url='login_page')
def account_place_order(request):
    customer = Customer.objects.get(user=request.user)
    cart = Cart.objects.get(customer=customer)
    cart_items = CartItem.objects.filter(cart=cart)

    new_order = Order.objects.create(customer=customer)
    total_price = 0

    for item in cart_items:
        OrderItem.objects.create(
            order=new_order, product=item.product, quantity=item.quantity, price=item.product.price)
        total_price += (item.quantity * item.product.price)

    print("Total Price:", total_price)
    new_order.total_price = total_price
    new_order.save()

    cart_items.delete()

    return redirect(reverse('account_dashboard'))


#------------------------------------------------------------------------------------------------------------------------------#


@login_required(login_url='login_page')
def account_orders(request):
    orders = Order.objects.filter(
        customer=request.user.customer).order_by('-order_date')

    context = {
        'title': 'Orders',
        'orders': orders,
    }

    return render(request, 'accounts/account_orders.html', context)


#------------------------------------------------------------------------------------------------------------------------------#


@login_required(login_url='login_page')
def account_view_order(request, order_id):
    # If order does not exist, redirect the user to their orders
    try:
        order = Order.objects.get(id=order_id)
        order_items = OrderItem.objects.filter(order=order)

        # We have to ensure that users can't see orders that don't belong to them.
        # Therefore we have to make sure that the user who is attempting to view
        # a particular order is the person who ordered it.
        if (str(order.customer) != str(request.user)):
            return redirect('account_orders')

        items_in_order = []

        for item in order_items:
            items_in_order.append(item)

        context = {
            'title': 'View Order',
            'order': order,
            'items_in_order': items_in_order,
        }

        return render(request, 'accounts/account_view_order.html', context)
    except:
        return redirect('account_orders')


#------------------------------------------------------------------------------------------------------------------------------#

@login_required(login_url='login_page')
def account_cancel_order(request, order_id):
    order = Order.objects.get(id=order_id)

    if (order.status != 'OR' or order.customer != request.user.customer):
        return redirect('account_view_order', order_id=order_id)
    else:
        order.delete()

    return redirect('account_dashboard')


#------------------------------------------------------------------------------------------------------------------------------#


@login_required(login_url='login_page')
def account_info(request):
    user = User.objects.get(username=request.user)
    customer = Customer.objects.get(user=user)

    context = {
        'title': 'Info',
        'user': user,
        'customer': customer,
    }

    return render(request, 'accounts/account_settings.html', context)


#------------------------------------------------------------------------------------------------------------------------------#


@login_required(login_url='login_page')
def account_info_change(request, form_type):
    if request.method == 'POST':
        user = User.objects.get(username=request.user)

        if form_type == 'account_credentials':
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']

            user.first_name = first_name
            user.last_name = last_name
            user.email = email

            user.save()
        elif form_type == 'account_billing':
            customer = Customer.objects.get(user=user)

            address_line_1 = request.POST['address_line_1']
            address_line_2 = request.POST['address_line_2']
            city = request.POST['city']
            state = request.POST['state']
            zipcode = request.POST['zipcode']

            customer.address_line_1 = address_line_1
            customer.address_line_2 = address_line_2
            customer.city = city
            customer.state = state
            customer.zipcode = zipcode

            customer.save()
        else:
            return redirect('account_dashboard')

        return redirect('account_info')
    else:
        return redirect('account_dashboard')


#------------------------------------------------------------------------------------------------------------------------------#
