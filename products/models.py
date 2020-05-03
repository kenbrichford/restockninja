from django.db import models
from django.utils.text import slugify
from django.utils.crypto import get_random_string
from mptt.models import MPTTModel, TreeForeignKey

def product_key():
    while True:
        key = get_random_string(
            length=7,
            allowed_chars='BCDFGHJKLMNPQRSTVWXYZ0123456789'
        )
        
        if not Product.objects.filter(pk=key).exists():
            return key

def category_key():
    while True:
        key = get_random_string(
            length=5,
            allowed_chars='BCDFGHJKLMNPQRSTVWXYZ0123456789'
        )
        
        if not Category.objects.filter(pk=key).exists():
            return key

class Base(models.Model):
    name = models.CharField(max_length=500)
    slug = models.SlugField(max_length=500, editable=False)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Product(Base):
    id = models.CharField(primary_key=True, max_length=7, default=product_key)
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, null=True)
    upc = models.CharField(max_length=13, blank=True, null=True)
    thumbnail = models.URLField()
    variants = models.ManyToManyField('self')

    def get_absolute_url(self):
        return '/products/%s/%s/' % (self.slug, self.pk)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        
        return super(Product, self).save(*args, **kwargs)

class Image(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    url = models.URLField()
    primary = models.BooleanField(default=False)

class Category(MPTTModel, Base):
    id = models.CharField(primary_key=True, max_length=5, default=category_key)
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )

    class Meta:
        verbose_name_plural = 'categories'

    class MPTTMeta:
        order_insertion_by = ['name']

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)

        return super(Category, self).save(*args, **kwargs)

class Brand(models.Model):
    name = models.CharField(max_length=20)
    slug = models.SlugField(max_length=20, unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)

        return super(Brand, self).save(*args, **kwargs)
