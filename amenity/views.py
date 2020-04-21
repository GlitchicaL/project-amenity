from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import Product, Cart
from accounts.models import Customer


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


def products(request):
    userCategory = request.GET.get('category', '')

    if (userCategory == ''):  # Display featured products only on the products page
        product_list = Product.objects.filter(featured=True)
    else:
        product_list = Product.objects.filter(category=userCategory)

    context = {
        'title': 'Products',
        'product_list': product_list,
    }

    return render(request, 'amenity/products.html', context)


def products_filter(request):
    userCategory = request.GET.get('category', '')

    product_list = Product.objects.filter(
        category=userCategory).values()

    JsonTxt = list(product_list)

    return JsonResponse(JsonTxt, safe=False)


def products_add_to_cart(request, product_to_add):
    # Get the product to add, the customer that requested it, and his/her cart
    product = Product.objects.get(name=product_to_add)
    customer = Customer.objects.get(user=request.user)
    cart = Cart.objects.get(customer=customer)

    cart.set_product_in_cart(product)
    cart.save()

    return redirect(reverse('account_dashboard', args=[request.user]))


def products_remove_from_cart(request, product_to_remove, row, call=''):
    # NOTE: Easier way to remove items from the cart via AJAX calls?

    # Get the customer, and his/her cart
    customer = Customer.objects.get(user=request.user)
    cart = Cart.objects.get(customer=customer)

    # Convert row from str to int, grab the products currently in the cart, then remove the item
    row = int(row)
    products = cart.get_products_in_cart()
    products.pop(row)

    # Reset cart to empty str temporarily
    cart.products_in_cart_text = ''

    # Re-add items to cart
    for product in products:
        cart.products_in_cart_text += (product + '\n')

    cart.save()

    return redirect(reverse('account_cart', args=[request.user]))
