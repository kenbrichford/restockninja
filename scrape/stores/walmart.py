import os
from scrape.data_structures import Link, Price, Listing, Product

class Walmart:
    items_per_request = 20
    call_limit = 5000

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
        if data.get('items'):
            return data.get('items')
        else:
            return []
    
    def parse_product_data(self, item):
        name = item.get('name')
        brand = item.get('brandName')
        if item.get('categoryPath') == 'UNNAV':
            category = []
        else:
            category = item.get('categoryPath').split('/')[1:]
        upc = item.get('upc')
        thumbnail = item.get('thumbnailImage')
        variants = item.get('variants')

        return Product(name, brand, category, upc, thumbnail, variants)
    
    def parse_image_data(self, item):
        images = []

        for image in item.get('imageEntities'):
            if image.get('entityType') == 'PRIMARY':
                primary = True
            else:
                primary = False

            images.append({'url': image.get('largeImage'), 'primary': primary})

        return images
    
    def parse_listing_data(self, item):
        return Listing(str(item.get('itemId')), item.get('productUrl'))

    def parse_price_data(self, item):
        if item.get('availableOnline') and not item.get('marketplace'):
            price = item.get('salePrice') * 100
            shipping = item.get('standardShipRate') * 100
            available = item.get('availableOnline')
        
        else:
            price = None
            shipping = None
            available = False 
        
        return Price(price, shipping, available)

