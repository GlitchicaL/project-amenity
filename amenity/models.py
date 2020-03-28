from django.db import models


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
