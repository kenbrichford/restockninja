import os
from scrape.data_structures import Link, Price, Listing, Product

class Walmart:
    items_per_request = 20
    call_limit = 5000
    sku_pattern = r'(?<=\/)\d{9}$'

    def create_url(self, **kwargs):
        skus = kwargs.get('skus', None)
        upc = kwargs.get('upc', None)
        
        params = {
            'apiKey': os.getenv('WALMART_API_KEY'),
            'ids': skus
        }

        if skus:
            params['ids'] = skus
        elif upc:
            params['upc'] = upc

        endpoint = 'http://api.walmartlabs.com/v1/items'

        return Link(endpoint, params)
    
    def get_items(self, data):
        return data.get('items')
    
    def parse_product_data(self, item):
        name = item.get('name')
        brand = item.get('brandName')
        category = item.get('categoryPath').split('/')[1:]
        upc = item.get('upc')
        thumbnail = item.get('thumbnailImage')
        variants = item.get('variants')

        return Product(name, brand, category, upc, thumbnail, variants)
    
    def parse_image_data(self, item):
        images = []

        primary = next((i for i in item.get('imageEntities') if i.get('entityType') == 'PRIMARY'), None)

        if primary:
            images.append(primary.get('largeImage'))

        for image in [i for i in item.get('imageEntities') if i != primary]:
            images.append(image.get('largeImage'))

        return images
    
    def parse_listing_data(self, item):
        return Listing(str(item.get('itemId')), item.get('productUrl'))

    def parse_price_data(self, item):
        if item.get('availableOnline') and not item.get('marketplace'):
            price = item.get('salePrice') * 100
            shipping = item.get('standardShipRate') * 100
            availability = item.get('availableOnline')
        
        else:
            price = None
            shipping = None
            availability = False 
        
        return Price(price, shipping, availability)

