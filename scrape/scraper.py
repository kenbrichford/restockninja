import re
import requests
import threading
from django.db import connection
from multiprocessing import Process, Queue
from products.models import Product, Image, Brand, Category
from listings.models import Listing, Vendor, Price
from .stores import import_stores

class Scraper:
    def __init__(self, vendor_name):
        self.vendor_name = vendor_name
    
    def create_store(self):
        if self.vendor_name == 'Best Buy':
            self.store = import_stores.BestBuy()  
        elif self.vendor_name == 'Walmart':
            self.store = import_stores.Walmart()   
        elif self.vendor_name == 'Target':
            self.store = import_stores.Target()

    def parse_store_data(self, scrape_type, scrape_string):
        self.create_store()
        
        if scrape_type == 'url':        
            url = self.store.create_url(skus=scrape_string)
        
        elif scrape_type == 'upc':
            url = self.store.create_url(upc=scrape_string)
            
        response = requests.get(url.endpoint, params=url.params)
        
        return self.store.get_items(response.json())

    def create_data_dict(self, item):
        self.data = {
            self.vendor_name: {
                'product': self.store.parse_product_data(item),
                'image': self.store.parse_image_data(item),
                'listing': self.store.parse_listing_data(item),
                'price': self.store.parse_price_data(item),
            }
        }
    
    def create_product_data(self):
        if self.data.get('Walmart'):
            product_data = self.data.get('Walmart').get('product')
        else:
            product_data = self.data.get(self.vendor_name).get('product')
        
        if not product_data.thumbnail:
            product_data.thumbnail = next((val.get('product').thumbnail for key, val in self.data.items()
                if val.get('product').thumbnail), '') 

        product_data.variants = next(({'vendor_name': key, 'skus': val.get('product').variants}
            for key, val in self.data.items() if val.get('product').variants), {})
        
        return product_data
    
    def scrape_other_vendors(self):
        other_vendors = Vendor.objects.exclude(name=self.vendor_name)

        upc = self.data.get(self.vendor_name).get('product').upc

        q = Queue()
        for vendor in other_vendors:
            scraper = Scraper(vendor.name)
            Process(target=scraper.scrape, args=('upc', upc, q)).start()
            self.data.update(q.get())
    
    def scrape_by_url(self):
        self.scrape_other_vendors()

        product_data = self.create_product_data()

        image_data = max((val['image'] for key, val in self.data.items()), key=len)

        self.product = create_product(product_data)
        
        for index, url in enumerate(image_data):
            threading.Thread(target=upload_image, args=(self.product, index, url)).start()
        
        for vendor_name, parsed_data in self.data.items():
            threading.Thread(target=upload_listing, args=(self.product, vendor_name, parsed_data)).start()

        variants = get_variants(product_data, self.product)
        for variant in variants:
            threading.Thread(target=self.product.variants.add, args=(variant,)).start()
        self.product.save()
    
    def scrape(self, scrape_type, scrape_string, q=None):
        items = self.parse_store_data(scrape_type, scrape_string)

        if items:
            item = items[0]

            self.create_data_dict(item)

            if scrape_type == 'upc':
                q.put(self.data)
            
            elif scrape_type == 'url':
                self.scrape_by_url()

def create_product(product_data):
    brand, brand_created = Brand.objects.get_or_create(
        name=product_data.brand
    )
    
    parent_category = None
    for category in product_data.category:
        category, category_created = Category.objects.get_or_create(
            name=category,
            parent=parent_category
        )
        parent_category = category

    product, product_created = Product.objects.get_or_create(
        upc=product_data.upc,
        defaults={
            'name': product_data.name,
            'brand': brand,
            'category': category,
            'thumbnail': product_data.thumbnail
        }
    )

    return product

def get_variants(product_data, product):
    variant_vendor = product_data.variants.get('vendor_name')
    variant_listings = Listing.objects.filter(
        vendor__name=variant_vendor,
        sku__in=product_data.variants.get('skus')
    )
    
    return Product.objects.filter(listing__in=variant_listings).exclude(id=product.id)

def upload_price(listing, parsed_data):
    # listing.url = parsed_data.url

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

    # listing.save()

def upload_image(product, index, url):
    primary = True if index == 0 else False
    image = Image(product=product, url=url, primary=primary)
    image.save()

def upload_listing(product, vendor_name, parsed_data):
    vendor = Vendor.objects.get(name=vendor_name)

    listing_data = parsed_data.get('listing')
    
    listing, created = Listing.objects.get_or_create(
        product=product,
        vendor=vendor,
        sku=listing_data.sku,
        defaults = {'url': listing_data.url}
    )

    upload_price(listing, parsed_data.get('price'))        
