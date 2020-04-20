from django.contrib import admin
from .models import Listing, Vendor

class ListingAdmin(admin.ModelAdmin):
    readonly_fields = ('url',)

admin.site.register(Listing, ListingAdmin)
admin.site.register(Vendor)
