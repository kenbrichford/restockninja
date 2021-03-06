from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Product, Category, Brand
from .forms import ProductForm
from listings.models import Listing

class ListingInline(admin.TabularInline):
    model = Listing
    exclude = ('url',)
    extra = 1

class CategoryInline(admin.TabularInline):
    model = Category
    fields = ('name',)
    extra = 1
    show_change_link = True

class ProductAdmin(admin.ModelAdmin):
    form = ProductForm
    readonly_fields = ('id', 'upc')
    inlines = [ListingInline]

class CategoryAdmin(MPTTModelAdmin):
    readonly_fields = ('id',)
    inlines = [CategoryInline]

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Brand)
