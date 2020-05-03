from django.db import models
from products.models import Product

class Email(models.Model):
    address = models.EmailField()

    def __str__(self):
        return self.address

class Alert(models.Model):
    email = models.ForeignKey('Email', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    verify = models.BooleanField(default=True)
    is_confirmed = models.BooleanField(default=False)
    created_time = models.DateTimeField(auto_now=True)
