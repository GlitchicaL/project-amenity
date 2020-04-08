from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.db import IntegrityError

from .models import Customer


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
        Customer.objects.create(user=user)

        # Login the user and redirect them to their dashboard
        login(request, user)
        return redirect('account_dashboard', username=username)
    else:
        return redirect('account')


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


def logout_account(request):
    logout(request)
    return redirect('account')


# Every function below this comment REQUIRES the user to be logged in!
@login_required(login_url='account')
def account_dashboard(request, username):
    user = User.objects.get(username=username)

    context = {
        'title': 'Dashboard',
        'user': user,
    }

    return render(request, 'accounts/account_dashboard.html', context)


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
