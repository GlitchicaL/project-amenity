from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

from .models import *
from accounts.models import Customer

import json


# Create your views here.
def home(request):
    featured_product_list = Product.objects.filter(featured=True)[:4]
    featured_categories = ['Tables', 'Lights', 'Chairs']

    context = {
        'title': 'Home',
        'featured_product_list': featured_product_list,
        'featured_categories': featured_categories,
    }

    return render(request, 'amenity/home.html', context)


#------------------------------------------------------------------------------------------------------------------------------#


def products(request):
    userCategory = request.GET.get('category', '')

    print(userCategory)

    if (userCategory == ''):  # Display featured products only on the products page
        product_list = Product.objects.filter(featured=True)
    else:
        product_list = Product.objects.filter(category=userCategory)

    context = {
        'title': 'Products',
        'product_list': product_list,
    }

    return render(request, 'amenity/products.html', context)


#------------------------------------------------------------------------------------------------------------------------------#


def products_filter(request):
    userCategory = request.GET.get('category', '')

    product_list = Product.objects.filter(
        category=userCategory).values()

    JsonTxt = list(product_list)
    return JsonResponse(JsonTxt, safe=False)


#------------------------------------------------------------------------------------------------------------------------------#


@require_http_methods(["POST"])
@login_required(login_url='login_page')
def products_add_to_cart(request):
    # Make sure the request method is POST, if not return error
    if (request.method != 'POST'):
        JsonTxt = 'Error'
        return JsonResponse(JsonTxt, safe=False)

    data = json.loads(request.body)
    productId = data['productId']

    product = Product.objects.get(id=productId)
    customer = Customer.objects.get(user=request.user)
    cart = Cart.objects.get(customer=customer)

    try:  # Attempt to see if that item already exists in cart
        cart_item = CartItem.objects.filter(cart=cart).get(product=product)
        cart_item.quantity += 1  # If item already exists, increase quantity by 1
        cart_item.save()
    except:  # Exception is thrown when item does not already exist in the cart
        cart_item = CartItem(cart=cart, product=product, quantity=1)
        cart_item.save()

    JsonTxt = 'Item added to cart!'
    return JsonResponse(JsonTxt, safe=False)
