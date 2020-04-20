from django.db import models
from django.utils.text import slugify
from django.utils.crypto import get_random_string
from mptt.models import MPTTModel, TreeForeignKey

def create_tag(model_type):
    while True:
        tag = get_random_string(
            length=7,
            allowed_chars='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        )
        
        if not model_type.objects.filter(tag=tag).exists():
            return tag

class Base(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, editable=False)
    tag = models.CharField(max_length=7, unique=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Product(Base):
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    featured = models.BooleanField(default=False)
    upc = models.CharField(max_length=12, unique=True)
    thumbnail = models.URLField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self.tag = create_tag(Product) if not self.tag else self.tag
        
        return super(Product, self).save(*args, **kwargs)

class Image(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    url = models.URLField()
    primary = models.BooleanField(default=False)

class Category(MPTTModel, Base):
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
        self.tag = create_tag(Category) if not self.tag else self.tag

        return super(Category, self).save(*args, **kwargs)

class Brand(models.Model):
    name = models.CharField(max_length=20)
    slug = models.SlugField(max_length=20, unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)

        return super(Brand, self).save(*args, **kwargs)
