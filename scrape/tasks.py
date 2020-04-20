from __future__ import absolute_import, unicode_literals
import time
import requests
import threading
from celery import shared_task
from django.utils import timezone
from django.core.management.base import BaseCommand
from datetime import timedelta
from listings.models import Listing, Price, Vendor
from .stores import import_stores

def upload_data(listing, parsed_data):
    listing.url = parsed_data.url

    last_price = Price.objects.filter(listing=listing).order_by('-updated_time').first()

    if last_price and last_price.price == parsed_data.price\
        and last_price.shipping == parsed_data.shipping:
        last_price.save()

    else:
        price = Price.objects.create(
            listing = listing,
            price = parsed_data.price,
            shipping = parsed_data.shipping,
            availability = parsed_data.availability
        )
        
        price.save()

    listing.save()

def create_store(vendor_name):
    if vendor_name == 'Best Buy':
        store = import_stores.BestBuy()
    
    elif vendor_name == 'Walmart':
        store = import_stores.Walmart()
    
    elif vendor_name == 'Target':
        store = import_stores.Target()
    
    return store

@shared_task
def scrape(vendor_name, path=None):
    if not path:
        one_minute_ago = timezone.now() - timedelta(minutes=1)

        listings = Listing.objects.filter(updated_time__lte=one_minute_ago, vendor__name=vendor_name)\
            .order_by('updated_time')
    
    store = create_store(vendor_name)

    if listings:
        truncated_listings = {i.sku: i for i in listings[store.items_per_request]}

        url = store.create_url(truncated_listings)
        
        response = requests.get(url.endpoint, params=url.params)
        
        items = store.get_items(response.json())
        
        if items:
            for item in items:
                parsed_data = store.parse_data(item)
                
                listing = truncated_listings.pop(parsed_data.sku)
                
                upload_data(listing, parsed_data)
        
        else:
            print('No items were returned from this request: %s' % response.text, flush=True)

        for listing in list(truncated_listings.values()):
            listing.save()
        
def single_scrape(vendor_name, path):
    store = create_store(vendor_name)

    url = store.create_url()
        
    response = requests.get(url.endpoint, params=url.params)
    
    items = store.get_items(response.json())
    
    if items:
        for item in items:
            parsed_data = store.parse_data(item)

def get_sku(pattern, url):
    try:
        sku = re.search(pattern, url.path).group(0)
    except AttributeError:
        sku = None
    
    return sku