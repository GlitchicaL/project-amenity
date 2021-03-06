from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.home, name="home"),

    path('products/', views.products, name="products"),
    path('products/filter/', views.products_filter, name="products_filter"),

    path('products/add-to-cart/', views.products_add_to_cart),
]
