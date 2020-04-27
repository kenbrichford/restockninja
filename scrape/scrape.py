import requests
from multiprocessing import Process, Queue
from products.models import Product, Image, Brand, Category
from listings.models import Listing, Vendor, Price
from .stores import import_stores

class Scrape:
    def __init__(self, vendor_name):
        self.vendor_name = vendor_name
        self.store = self.create_store()
    
    def create_store(self):
        if self.vendor_name == 'Best Buy':
            return import_stores.BestBuy()  
        elif self.vendor_name == 'Walmart':
            return import_stores.Walmart()   
        elif self.vendor_name == 'Target':
            return import_stores.Target()

    def get_store_items(self, url):
        response = requests.get(url.endpoint, params=url.params)
        return self.store.get_items(response.json())
    
    def create_data_dict(self, item):
        return {self.vendor_name: {
            'product': self.store.parse_product_data(item),
            'image': self.store.parse_image_data(item),
            'listing': self.store.parse_listing_data(item),
            'price': self.store.parse_price_data(item),
        }}
    
    def format_product_data(self, data):
        if data.get('Walmart'):
            product_data = data.get('Walmart').get('product')
        else:
            product_data = data.get(self.vendor_name).get('product')
        
        if not product_data.thumbnail:
            product_data.thumbnail = next((store_data.get('product').thumbnail\
                for store, store_data in data.items()\
                    if store_data.get('product').thumbnail), '')
        
        product_data.variants = next(({'vendor_name': store, 'skus': store_data.get('product').variants}\
            for store, store_data in data.items() if store_data.get('product').variants), {})

        return product_data
    
    def scrape_by_upc(self, query, queue):
        url = self.store.create_url(upc=query)
        items = self.get_store_items(url)

        if items:
            data = self.create_data_dict(items[0])
            queue.put(data)
        else:
            queue.put({self.vendor_name: None})
    
    def scrape_by_url(self, query):
        url = self.store.create_url(skus=query)
        items = self.get_store_items(url)

        if items:
            data = self.create_data_dict(items[0])
            
            other_vendors = Vendor.objects.exclude(name=self.vendor_name)
            
            upc = data.get(self.vendor_name).get('product').upc
            
            if upc:
                queue = Queue()
                for vendor in other_vendors:
                    scrape = Scrape(vendor.name)
                    Process(target=scrape.scrape_by_upc, args=(upc, queue)).start()
                    data.update(queue.get())
            
            data = {store: store_data for store, store_data in data.items() if store_data}

            product_data = self.format_product_data(data)

            image_data = max((store_data.get('image', []) for store, store_data in data.items()), key=len)

            product = upload_product(product_data)[0]
            
            for image in image_data:
                upload_image(product, image)
            
            for store, store_data in data.items():
                upload_listing(product, store, store_data)

            if product_data.variants:
                variants = get_variants(product_data, product)
                for variant in variants:
                    product.variants.add(variant)
                product.save()
            
            return product
        
        return None
    
    def scrape_by_listing(self, listing):
        url = self.store.create_url(skus=listing.sku)
        items = self.get_store_items(url)

        if items:
            price_data = self.store.parse_price_data(items[0])
            upload_price(listing, price_data)

        listing.save()

def upload_product(product_data):
    brand = Brand.objects.get_or_create(name=product_data.brand)[0]
    
    if product_data.category:
        parent = None
        for cat in product_data.category:
            category = Category.objects.get_or_create(name=cat, parent=parent)[0]
            parent = category
    else:
        category = None

    return Product.objects.get_or_create(
        upc=product_data.upc,
        name=product_data.name,
        defaults={
            'brand': brand,
            'category': category,
            'thumbnail': product_data.thumbnail
        }
    )

def upload_image(product, image):
    image = Image(product=product, url=image.get('url'), primary=image.get('primary'))
    image.save()

def upload_price(listing, parsed_data):
    last_price = Price.objects.filter(listing=listing).order_by('-updated_time').first()

    if last_price and last_price.price == parsed_data.price\
        and last_price.shipping == parsed_data.shipping:
        last_price.save()

    else:
        price = Price.objects.create(
            listing = listing,
            price = parsed_data.price,
            shipping = parsed_data.shipping,
            available = parsed_data.available
        )
        
        price.save()

def upload_listing(product, vendor_name, parsed_data):
    vendor = Vendor.objects.get(name=vendor_name)

    listing_data = parsed_data.get('listing')
    
    listing = Listing.objects.get_or_create(
        product=product,
        vendor=vendor,
        sku=listing_data.sku,
        defaults = {'url': listing_data.url}
    )

    upload_price(listing[0], parsed_data.get('price'))    

def get_variants(product_data, product):
    variant_vendor = product_data.variants.get('vendor_name')
    variant_listings = Listing.objects.filter(
        vendor__name=variant_vendor,
        sku__in=product_data.variants.get('skus')
    )
    
    return Product.objects.filter(listing__in=variant_listings).exclude(id=product.pk)    
