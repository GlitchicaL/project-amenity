from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect

from .models import Product

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
