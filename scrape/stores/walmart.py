import os
from scrape.data_structures import Link, Price, Listing, Product

class Walmart:
    items_per_request = 20
    call_limit = 5000
    free_shipping_minimum = 3500

    def create_url(self, **kwargs):
        skus = kwargs.get('skus', None)
        upc = kwargs.get('upc', None)
        keyword = kwargs.get('keyword', None)
        
        params = {
            'apiKey': os.getenv('WALMART_API_KEY')
        }

        endpoint = 'http://api.walmartlabs.com/v1/items'

        if skus:
            params['ids'] = skus
        elif upc:
            params['upc'] = upc
        elif keyword:
            endpoint = 'http://api.walmartlabs.com/v1/search'
            params['query'] = keyword
        

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
        
        if item.get('imageEntities'):
            for image in item.get('imageEntities'):
                if image.get('entityType') == 'PRIMARY':
                    primary = True
                else:
                    primary = False

                images.append({'url': image.get('largeImage'), 'primary': primary})
        elif item.get('largeImage'):
            images.append({'url': item.get('largeImage'), 'primary': True})

        return images[:5]
    
    def parse_listing_data(self, item):
        sku = str(item.get('itemId'))
        url = 'https://www.walmart.com/ip/%s' % sku

        return Listing(sku, url)

    def parse_price_data(self, item):
        if item.get('availableOnline') and not item.get('marketplace'):
            price = item.get('salePrice') * 100
            if item.get('standardShipRate'):
                shipping = item.get('standardShipRate') * 100
            else:
                shipping = 0 if price > self.free_shipping_minimum else None
            available = item.get('availableOnline')
        
        else:
            price = None
            shipping = None
            available = False 
        
        return Price(price, shipping, available)

