import os
from scrape.data_structures import Link, Price

class Ebay:
    items_per_request = 1
    call_limit = 5000
    url = ''

    def create_url(self, listings):
        params = {
            'SERVICE-VERSION': '1.0.0',
            'SECURITY-APPNAME': os.getenv('EBAY_APP_ID'),
            'OPERATION-NAME': 'findItemsByProduct',
            'RESPONSE-DATA-FORMAT': 'JSON',
            'productId.@type': 'ReferenceID',
            'productId': listings[0].sku,
            'paginationInput.entriesPerPage': 1,
            'sortOrder': 'PricePlusShippingLowest',
            'itemFilter(0).name': 'Condition',
            'itemFilter(0).value': 1000,
            'itemFilter(1).name': 'ListingType',
            'itemFilter(1).value': 'StoreInventory',
            'itemFilter(2).name': 'LocatedIn',
            'itemFilter(2).value': 'US',
            'itemFilter(3).name': 'MinQuantity',
            'itemFilter(3).value': 10,
        }

        endpoint = 'https://svcs.ebay.com/services/search/FindingService/v1'

        return Link(endpoint, params)

    def get_items(self, data):
        response = data.get('findItemsByProductResponse')
        
        if response[0].get('ack')[0] == 'Success':
            self.url = response[0].get('itemSearchURL')[0]

            return response[0].get('searchResult')[0].get('item')

        else:
            return None

    def parse_data(self, item):
        sku = item.get('productId')[0].get('__value__')

        if item.get('onlineAvailability'):
            price = item.get('salePrice') * 100
            shipping = item.get('shippingCost') * 100 if item.get('shippingCost') else 0
        
        else:
            price = None
            shipping = None
        
        available = item.get('onlineAvailability')
        

        return Price(sku, self.url, price, shipping, available)
    