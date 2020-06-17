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
    order_date = models.DateTimeField(auto_now=False, auto_now_add=True)
    total_price = models.DecimalField(
        max_digits=7, decimal_places=2, default=0.00)

    status_list = [
        ('OR', 'Ordered'),
        ('SH', 'Shipped'),
        ('DE', 'Delivered'),
    ]

    status = models.CharField(choices=status_list, default='OR', max_length=2)
    status_date = models.DateField(auto_now=True)

    def __str__(self):
        return 'Order ' + str(self.id) + ' by ' + self.customer.user.username


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=7, decimal_places=2, default=0.00)


class Cart(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)

    def __str__(self):
        return self.customer.user.username + '\'s' + ' Cart'

    def setPrice(self, price):
        self.price = price


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
