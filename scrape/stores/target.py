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
            'excludes': 'bulk_ship,rating_and_review_reviews,question_answer_statistics,promotion,rating_and_review_statistics,esp',
            'key': os.getenv('TARGET_API_KEY'),
            'count': 10
        }

        if skus:
            endpoint = 'https://redsky.target.com/v2/pdp/tcin/%s' % skus
        elif upc or keyword:
            endpoint = 'https://redsky.target.com/v1/plp/search'
            params['keyword'] = upc if upc else keyword

        return Link(endpoint, params)

    def get_items(self, data):
        if isinstance(data, list):
            return data
        elif data.get('product'):
            if data.get('product').get('item'):
                return [data]
        else:
            response = data.get('search_response', {}).get('items', {}).get('Item')
            if response and not response[0].get('error_message'):
                return response
            
        return []
    
    def parse_product_data(self, item):
        if item.get('product'):
            item = item.get('product').get('item')
            name = item.get('product_description', {}).get('title')
            brand = item.get('product_brand', {}).get('brand', '')
            category = [item.get('product_classification', {}).get('item_type', {}).get('name').title()]
            upc = item.get('upc')
            if item.get('enrichment', {}).get('images'):
                thumbnailData = item.get('enrichment').get('images')[0]
                thumbnail = thumbnailData.get('base_url')
                thumbnail += thumbnailData.get('primary')
        else:
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

        if item.get('product'):
            item = item.get('product').get('item')
            if item.get('enrichment', {}).get('images'):
                imageData = item.get('enrichment').get('images')[0]
                base_url = imageData.get('base_url')
                primary = base_url + imageData.get('primary')

                images.append({'url': primary, 'primary': True})

                if imageData.get('alternate_urls'):
                    for image in imageData.get('alternate_urls'):
                        images.append({'url': base_url + image, 'primary': False})
        else:
            if item.get('images'):
                base_url = item.get('images')[0].get('base_url')
                primary = base_url + item.get('images')[0].get('primary')

                images.append({'url': primary, 'primary': True})
                
                if item.get('images')[0].get('alternate_urls'):
                    for image in item.get('images')[0].get('alternate_urls'):
                        images.append({'url': base_url + image, 'primary': False})

        return images[:5]
    
    def parse_listing_data(self, item):
        if item.get('product'):
            sku = item.get('product').get('item').get('tcin')
            url = item.get('product').get('item').get('buy_url')
        else:
            sku = item.get('tcin')
            url = 'https://www.target.com%s' % item.get('url')

        return Listing(sku, url)

    def parse_price_data(self, item):
        if item.get('product') and item.get('product').get('available_to_promise_network', {}).get('availability_status') == 'IN_STOCK':
            price = item.get('product').get('price', {}).get('offerPrice', {}).get('price') * 100
            shipping = 0 if price > self.free_shipping_minimum else None
            available = True
        elif item.get('availability_status') and item.get('availability_status') == 'IN_STOCK':
            price = item.get('offer_price').get('price') * 100
            shipping = 0 if price > self.free_shipping_minimum else None
            available = True
        else:
            price = None
            shipping = None
            available = False

        return Price(price, shipping, available)