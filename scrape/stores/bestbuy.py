import os
from scrape.data_structures import Link, Price, Listing, Product

class BestBuy:
    items_per_request = 100
    call_limit = 50000

    def create_url(self, **kwargs):
        skus = kwargs.get('skus', None)
        upc = kwargs.get('upc', None)
        
        shown_attributes = [
            'sku', 'url', 'name', 'salePrice', 'categoryPath',
            'onlineAvailability', 'shippingCost', 'images', 'upc',
            'thumbnailImage', 'manufacturer', 'productVariations',
        ]

        params = {
            'apiKey': os.getenv('BESTBUY_API_KEY'),
            'show': ','.join(shown_attributes),
            'format': 'json',
            'pageSize': 100,
        }

        endpoint = 'https://api.bestbuy.com/v1/products'

        if skus:
            endpoint += '(sku in(%s))' % skus
        elif upc:
            endpoint += '(upc=%s)' % upc

        return Link(endpoint, params)

    def get_items(self, data):
        if data.get('products'):
            return data.get('products')
        else:
            return []

    def parse_product_data(self, item):
        name = item.get('name')
        brand = item.get('manufacturer')
        category = [c.get('name') for c in item.get('categoryPath')][1:]
        upc = item.get('upc')
        thumbnail = item.get('thumbnailImage')
        variants = [i.get('sku') for i in item.get('productVariations')]

        return Product(name, brand, category, upc, thumbnail, variants)
    
    def parse_image_data(self, item):
        images = []

        for image in item.get('images'):
            if int(image.get('width')) > 500 or int(image.get('height')) > 500:
                images.append({
                    'url': image.get('href'),
                    'primary': image.get('primary')
                })

        return images
    
    def parse_listing_data(self, item):
        return Listing(str(item.get('sku')), item.get('url'))

    def parse_price_data(self, item):
        if item.get('onlineAvailability'):
            price = item.get('salePrice') * 100
            shipping = item.get('shippingCost') * 100 if item.get('shippingCost') else 0
        
        else:
            price = None
            shipping = None
        
        available = item.get('onlineAvailability')

        return Price(price, shipping, available)