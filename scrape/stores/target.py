import os
from scrape.data_structures import Link, Price

class Target:
    items_per_request = 1
    free_shipping_minimum = 3500
    sku_pattern = r'(?<=(\/A-))\d{8}$'

    def create_url(self, listings):
        excluded_fields = [
            'esp',
            'taxonomy',
            'promotion',
            'bulk_ship',
            'rating_and_review_reviews',
            'rating_and_review_statistics',
            'question_answer_statistics'
        ]

        params = {
            'excludes': ','.join(excluded_fields),
        }

        endpoint = 'https://redsky.target.com/v2/pdp/tcin/%s' % listings[0].sku

        return Link(endpoint, params)

    def get_items(self, data):
        return [data.get('product')] if data.get('product').get('item') else []

    def parse_data(self, item):
        sku = item.get('item').get('tcin')
        url = item.get('item').get('buy_url')

        if item.get('available_to_promise_network').get('availability') == 'AVAILABLE':
            price = item.get('price').get('offerPrice').get('price') * 100
            shipping = 0 if price > self.free_shipping_minimum else None
            availability = True
        
        else:
            price = None
            shipping = None
            availability = False        

        return Price(sku, url, price, shipping, availability)