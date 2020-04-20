import os
from scrape.data_structures import Link, Price

class Walmart:
    items_per_request = 20
    call_limit = 5000
    sku_pattern = r'(?<=\/)\d{9}$'

    def create_url(self, listings):
        params = {
            'apiKey': os.getenv('WALMART_API_KEY'),
            'ids': ','.join([listing.sku for listing in listings])
        }

        endpoint = 'http://api.walmartlabs.com/v1/items'

        return Link(endpoint, params)
    
    def get_items(self, data):
        return data.get('items')

    def parse_data(self, item):
        sku = str(item.get('itemId'))

        url = item.get('productUrl')
        
        if item.get('availableOnline') and not item.get('marketplace'):
            price = item.get('salePrice') * 100
            shipping = item.get('standardShipRate') * 100
            availability = item.get('availableOnline')
        
        else:
            price = None
            shipping = None
            availability = False        
        
        return Price(sku, url, price, shipping, availability)

