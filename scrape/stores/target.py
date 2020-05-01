import os
import html
from scrape.data_structures import Link, Price, Listing, Product

class Target:
    items_per_request = 100
    free_shipping_minimum = 3500

    def create_url(self, **kwargs):
        skus = kwargs.get('skus', None)
        upc = kwargs.get('upc', None)
        keyword = kwargs.get('keyword', None)

        params = {
            'excludes': 'esp',
            'key': os.getenv('TARGET_API_KEY'),
            'count': 10
        }

        if skus:
            endpoint = 'https://redsky.target.com/v1/plp/collection/%s' % skus
        elif upc or keyword:
            endpoint = 'https://redsky.target.com/v1/plp/search'
            params['keyword'] = upc if upc else keyword

        return Link(endpoint, params)

    def get_items(self, data):
        response = data.get('search_response', {}).get('items', {}).get('Item')
        if response and not response[0].get('error_message'):
            return response
            
        return []
    
    def parse_product_data(self, item):
        name = html.unescape(item.get('title'))
        brand = item.get('brand')
        category = [item.get('merch_class').title()]
        upc = item.get('upc')
        if item.get('images'):
            thumbnail = item.get('images')[0].get('base_url')
            thumbnail += item.get('images')[0].get('primary')
        variants = []

        return Product(name, brand, category, upc, thumbnail, variants)
    
    def parse_image_data(self, item):
        images = []

        if item.get('images'):
            base_url = item.get('images')[0].get('base_url')
            primary = base_url + item.get('images')[0].get('primary')

            images.append({'url': primary, 'primary': True})
            
            if item.get('images')[0].get('alternate_urls'):
                for image in item.get('images')[0].get('alternate_urls'):
                    images.append({'url': base_url + image, 'primary': False})

        return images
    
    def parse_listing_data(self, item):
        sku = item.get('tcin')
        url = 'https://www.target.com%s' % item.get('url')

        return Listing(sku, url)

    def parse_price_data(self, item):
        if item.get('availability_status') == 'IN_STOCK':
            price = item.get('offer_price').get('price') * 100
            shipping = 0 if price > self.free_shipping_minimum else None
            available = True
        
        else:
            price = None
            shipping = None
            available = False

        return Price(price, shipping, available)