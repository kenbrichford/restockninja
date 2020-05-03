from django.db import models
from datetime import datetime
from products.models import Product

class Listing(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    vendor = models.ForeignKey('Vendor', on_delete=models.CASCADE)
    sku = models.CharField(max_length=20)
    url = models.URLField(max_length=500, blank=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['sku', 'vendor']

    def __str__(self):
        return '%s: %s' % (self.vendor, self.sku)

class Vendor(models.Model):
    name = models.CharField(max_length=20)
    image = models.ImageField(upload_to='vendors', blank=True)

    def __str__(self):
        return self.name

class Price(models.Model):
    listing = models.ForeignKey('Listing', on_delete=models.CASCADE)
    price = models.PositiveIntegerField(null=True)
    shipping = models.PositiveIntegerField(null=True)
    is_available = models.BooleanField()
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return '%s: %s' % (self.listing, self.created_time)