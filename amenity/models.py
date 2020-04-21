from django.db import models

from accounts.models import Customer


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=50, default='null')
    price = models.DecimalField(max_digits=7, decimal_places=2)
    category = models.CharField(max_length=50, default='null')
    description = models.TextField()
    featured = models.BooleanField()
    date_created = models.DateField(auto_now=False, auto_now_add=False)
    date_removed = models.DateField(auto_now=False, auto_now_add=False)

    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    products = models.TextField(default='', blank=True)
    order_date = models.DateTimeField(auto_now=False, auto_now_add=True)

    status_list = [
        ('OR', 'Ordered'),
        ('SH', 'Shipped'),
        ('DE', 'Delivered'),
    ]

    status = models.CharField(choices=status_list, default='OR', max_length=2)
    status_date = models.DateField(auto_now=True)

    def __str__(self):
        return 'Order ' + str(self.id) + ' by ' + self.customer.user.username

    def get_products_in_order(self):
        return self.products.splitlines()


class Cart(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)

    products_in_cart_text = models.TextField(default='', blank=True)

    def __str__(self):
        return self.customer.user.username + '\'s' + ' Cart'

    def set_product_in_cart(self, product):
        self.products_in_cart_text += str(product.id) + '\n'

    def get_products_in_cart(self):
        return self.products_in_cart_text.splitlines()
