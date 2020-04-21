from django.db import models

from django.contrib.auth.models import User


# Account Models
class Customer(models.Model):
    # Extends from django's user model using a one-to-one relationship
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    address_line_1 = models.CharField(
        "Address Line 1",
        max_length=50,
        blank=True
    )

    address_line_2 = models.CharField(
        "Address Line 2",
        max_length=50,
        blank=True
    )

    city = models.CharField(max_length=50, blank=True)
    state = models.CharField(max_length=50, blank=True)
    zipcode = models.IntegerField(null=True)

    def __str__(self):
        return self.user.username
