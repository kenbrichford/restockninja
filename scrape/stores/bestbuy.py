import os
from scrape.data_structures import Link, Price

class BestBuy:
    items_per_request = 100
    call_limit = 50000
    sku_pattern = r'(?<=\/)\d{7}(?=(\.p)$)'

    def create_url(self, listings):
        params = {
            'apiKey': os.getenv('BESTBUY_API_KEY'),
            'show': 'sku,url,salePrice,onlineAvailability,shippingCost',
            'format': 'json',
            'pageSize': '100',
        }

        endpoint = 'https://api.bestbuy.com/v1/products(sku in(%s))' % (
            ','.join([listing.sku for listing in listings])
        )

        return Link(endpoint, params)

    def get_items(self, data):
        return data.get('products')

    def parse_data(self, item):
        sku = str(item.get('sku'))
        url = item.get('url')

        if item.get('onlineAvailability'):
            price = item.get('salePrice') * 100
            shipping = item.get('shippingCost') * 100 if item.get('shippingCost') else 0
        
        else:
            price = None
            shipping = None
        
        availability = item.get('onlineAvailability')
        

        return Price(sku, url, price, shipping, availability)