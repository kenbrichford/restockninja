class Link:
    def __init__(self, endpoint, params):
        self.endpoint = endpoint
        self.params = params
    
class Sku:
    def __init__(self, vendor_name, sku):
        self.vendor_name = vendor_name
        self.sku = sku

class Price:
    def __init__(self, sku, url, price, shipping, availability):
        self.sku = sku
        self.url = url
        self.price = price
        self.shipping = shipping
        self.availability = availability