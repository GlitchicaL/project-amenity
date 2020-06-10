from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.db import IntegrityError

from .models import Customer
from amenity.models import Product, Order, OrderItem, Cart, CartItem

ERROR_MSGS = {
    '': '',
    'AC1': 'Passwords do not match.',
    'AC2': 'Username already exists!',
    'AL1': 'Incorrect username or password.',
}


#------------------------------------------------------------------------------------------------------------------------------#


def register_page(request, message=''):
    context = {
        'title': 'Register',
        'message': ERROR_MSGS[message],
    }

    return render(request, 'accounts/register.html', context)


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
            return redirect('create_account_error', message="AC1")

        # Create the user
        try:
            user = User.objects.create_user(username, email, password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
        except (IntegrityError):  # Exception raised if username already exists
            return redirect('create_account_error', message="AC2")

        # Assign user as a customer
        customer = Customer.objects.create(user=user)
        Cart.objects.create(customer=customer)

        # Login the user and redirect them to their dashboard
        login(request, user)
        return redirect('account_dashboard')
    else:
        return redirect('register_page')


#------------------------------------------------------------------------------------------------------------------------------#


def login_page(request, message=''):
    context = {
        'title': 'Login',
        'message': ERROR_MSGS[message],
    }

    return render(request, 'accounts/login.html', context)

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
            return redirect('login_error', message='AL1')


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


@login_required(login_url='login_page')
def account_add_to_cart(request, product_to_add):
    # TODO: Perform a check to see if the product is already in the cart, if it is, increase the quantity by 1.

    product = Product.objects.get(name=product_to_add)
    customer = Customer.objects.get(user=request.user)
    cart = Cart.objects.get(customer=customer)

    # Create a new CartItem row, we need the customer, his/her cart, the product to add, and the quantity.
    cart_item = CartItem(cart=cart, product=product, quantity=1)
    cart_item.save()

    return redirect(reverse('account_dashboard'))


#------------------------------------------------------------------------------------------------------------------------------#


@login_required(login_url='login_page')
def account_remove_from_cart(request, product_to_remove):
    # NOTE: Easier way to remove items from the cart via AJAX calls?

    # Get the customer, and his/her cart
    cart = Cart.objects.get(customer=request.user.customer)
    cart_item = CartItem.objects.filter(
        cart=cart).filter(product=product_to_remove)

    cart_item.delete()

    return redirect(reverse('account_cart'))


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

    for item in cart_items:
        OrderItem.objects.create(
            order=new_order, product=item.product, quantity=item.quantity, price=item.product.price)

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
        price_of_order = 0

        for item in order_items:
            items_in_order.append(item)
            price_of_order += item.price

        context = {
            'title': 'View Order',
            'order': order,
            'items_in_order': items_in_order,
            'price_of_order': price_of_order,
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
