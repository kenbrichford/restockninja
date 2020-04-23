class Link:
    def __init__(self, endpoint, params):
        self.endpoint = endpoint
        self.params = params

class Price:
    def __init__(self, price, shipping, available):
        self.price = price
        self.shipping = shipping
        self.available = available

class Listing:
    def __init__(self, sku, url):
        self.sku = sku
        self.url = url

class Product:
    def __init__(self, name, brand, category, upc, thumbnail, variants):
        self.name = name
        self.brand = brand
        self.category = category
        self.upc = upc
        self.thumbnail = thumbnail
        self.variants = variants