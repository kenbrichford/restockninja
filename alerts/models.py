from django.db import models
from products.models import Product

class Email(models.Model):
    address = models.EmailField()

    def __str__(self):
        return self.address

class Alert(models.Model):
    FREQUENCIES = [
        (604800, 'Weekly'),
        (86400, 'Daily'),
        (43200, 'Two per day'),
        (28800, 'Three per day'),
        (3600, 'Hourly'),
        (0, 'All updates'),
    ]

    email = models.ForeignKey('Email', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    is_confirmed = models.BooleanField(default=False)
    created_time = models.DateTimeField(auto_now_add=True)
    email_frequency = models.PositiveIntegerField(
        choices=FREQUENCIES,
        default=86400,
    )
    last_notified = models.DateTimeField(null=True)
