from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.db import IntegrityError

from .models import Customer
from amenity.models import Product, Order, Cart


# Account view allows user to login or create an account
def account(request):
    context = {
        'title': 'Login',
    }

    # If user is already logged in, redirect them to their dashboard. Otherwise allow them to create/login.
    if request.user.is_authenticated:
        return redirect('account_dashboard', username=request.user.username)
    else:
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
            return redirect('account')

        # Create the user
        try:
            user = User.objects.create_user(username, email, password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
        except (IntegrityError):  # Exception raised if username already exists
            return redirect('account')

        # Assign user as a customer
        customer = Customer.objects.create(user=user)
        Cart.objects.create(customer=customer)

        # Login the user and redirect them to their dashboard
        login(request, user)
        return redirect('account_dashboard', username=username)
    else:
        return redirect('account')


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
            return redirect('account_dashboard', username=username)
        else:
            return redirect('account')


#------------------------------------------------------------------------------------------------------------------------------#


def logout_account(request):
    logout(request)
    return redirect('account')


#------------------------------------------------------------------------------------------------------------------------------#


# Every function below this comment REQUIRES the user to be logged in!
@login_required(login_url='account')
def account_dashboard(request, username):
    user = User.objects.get(username=username)
    cart = Cart.objects.get(customer=user.customer)

    orders = Order.objects.filter(
        customer=user.customer).order_by('-order_date')[:3]
    products_in_cart = []
    price_of_cart = 0

    for product in cart.get_products_in_cart():
        product_id = int(product)
        products_in_cart.append(Product.objects.get(pk=product_id))

    for product in products_in_cart:
        price_of_cart += product.price

    context = {
        'title': 'Dashboard',
        'user': user,
        'orders': orders,
        'products_in_cart': products_in_cart,
        'price_of_cart': price_of_cart,
    }

    return render(request, 'accounts/account_dashboard.html', context)


#------------------------------------------------------------------------------------------------------------------------------#


@login_required(login_url='account')
def account_cart(request, username):
    cart = Cart.objects.get(customer=request.user.customer)

    products_in_cart = []
    price_of_cart = 0

    for product in cart.get_products_in_cart():
        product_id = int(product)
        products_in_cart.append(Product.objects.get(pk=product_id))

    for product in products_in_cart:
        price_of_cart += product.price

    context = {
        'title': 'Cart',
        'products_in_cart': products_in_cart,
        'price_of_cart': price_of_cart,
    }

    return render(request, 'accounts/account_cart.html', context)


#------------------------------------------------------------------------------------------------------------------------------#
# TODO: Make this function empty the user's cart!

def account_empty_cart(request, username):
    cart = Cart.objects.get(customer=request.user.customer)

    cart.products_in_cart_text = ''
    cart.save()

    return redirect('account_cart', username=username)


#------------------------------------------------------------------------------------------------------------------------------#


@login_required(login_url='account')
def account_place_order(request, username):
    # TODO: Make sure there are actually products in the cart, we don't want to place an empty order!

    customer = Customer.objects.get(user=request.user)
    cart = Cart.objects.get(customer=customer)

    Order.objects.create(
        customer=customer, products=cart.products_in_cart_text)

    cart.products_in_cart_text = ''
    cart.save()

    return redirect(reverse('account_dashboard', args=[username]))


#------------------------------------------------------------------------------------------------------------------------------#
# TODO: Make this function cancel orders that have the status 'Ordered (OR)'

def account_cancel_order(request, username, order_id):
    order = Order.objects.get(id=order_id)

    order.delete()

    return redirect('account_dashboard', username=username)


#------------------------------------------------------------------------------------------------------------------------------#


@login_required(login_url='account')
def account_orders(request, username):
    orders = Order.objects.filter(
        customer=request.user.customer).order_by('-order_date')

    context = {
        'title': 'Orders',
        'orders': orders,
    }

    return render(request, 'accounts/account_orders.html', context)


#------------------------------------------------------------------------------------------------------------------------------#


def account_view_order(request, username, order_id):
    order = Order.objects.get(id=order_id)

    products_in_order = []
    price_of_order = 0

    for product in order.get_products_in_order():
        product_id = int(product)
        products_in_order.append(Product.objects.get(pk=product_id))

    for product in products_in_order:
        price_of_order += product.price

    context = {
        'title': 'View Order',
        'order': order,
        'products_in_order': products_in_order,
        'price_of_order': price_of_order,
    }

    return render(request, 'accounts/account_view_order.html', context)


#------------------------------------------------------------------------------------------------------------------------------#


@login_required(login_url='account')
def account_info(request, username):
    user = User.objects.get(username=username)
    customer = Customer.objects.get(user=user)

    context = {
        'title': 'Info',
        'user': user,
        'customer': customer,
    }

    return render(request, 'accounts/account_settings.html', context)


#------------------------------------------------------------------------------------------------------------------------------#


@login_required(login_url='account')
def account_info_change(request, username, form_type):
    if request.method == 'POST':
        user = User.objects.get(username=username)

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
            return redirect('account_dashboard', username=username)

        return redirect('account_info', username=username)
    else:
        return redirect('account_dashboard', username=username)


#------------------------------------------------------------------------------------------------------------------------------#
