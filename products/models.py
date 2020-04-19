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
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=300, editable=False)
    tag = models.CharField(max_length=6, unique=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Product(Base):
    manufacturer = models.ForeignKey('Manufacturer', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    featured = models.BooleanField(default=False)
    image = models.ImageField(upload_to='products', blank=True)

    def save(self, *args, **kwargs):
        self.slug = '%s-%s' % (self.manufacturer.slug, slugify(self.name))

        if not self.tag:
            self.tag = create_tag(Product)
        
        return super(Product, self).save(*args, **kwargs)

class Category(MPTTModel, Base):
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )
    image = models.ImageField(upload_to='categories', blank=True)

    class Meta:
        verbose_name_plural = 'categories'

    class MPTTMeta:
        order_insertion_by = ['name']

    def save(self, *args, **kwargs):
        if self.parent:
            self.slug = '%s-%s' % (self.parent.slug, slugify(self.name))
        else:
            self.slug = slugify(self.name)

        if not self.tag:
            self.tag = create_tag(Category)

        return super(Category, self).save(*args, **kwargs)

class Manufacturer(models.Model):
    name = models.CharField(max_length=20)
    slug = models.SlugField(max_length=20)

    def __str__(self):
        return self.name
