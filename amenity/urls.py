from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.home, name="home"),

    path('products/', views.products, name="products"),
    path('products/filter/', views.products_filter, name="products_filter"),

    path(
        'products/add/<str:product_to_add>/',
        views.products_add_to_cart,
        name="products_add_to_cart"
    ),

    path(
        'products/remove/<str:product_to_remove>/<str:row>/',
        views.products_remove_from_cart,
        name="products_remove_from_cart"
    ),
]
