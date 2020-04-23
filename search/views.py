import re
from urllib.parse import unquote, urlparse
from django.contrib import messages
from django.shortcuts import redirect
from listings.models import Listing
from scrape.scrape import Scrape

stores = [
    {'name': 'Walmart', 'domain': 'walmart', 'pattern': r'(?<=\/)\d{9}$'},
    {'name': 'Best Buy', 'domain': 'bestbuy', 'pattern': r'(?<=\/)\d{7}(?=(\.p)$)'},
    {'name': 'Target', 'domain': 'target', 'pattern': r'(?<=(\/A-))\d{8}$'}
]

def get_sku(pattern, url_path):
    try:
        return re.search(pattern, url_path).group(0)
    except AttributeError:
        return None

def search(request):
    query = unquote(request.GET.get('query', None))
    url = urlparse(query)
    domain = url.netloc.split('.')[-2] if url.netloc else None
    store = next((store for store in stores if store.get('domain') == domain), None)

    if store:
        vendor_name = store.get('name')   
        sku = get_sku(store.get('pattern'), url.path)

        if vendor_name and sku:
            listing = Listing.objects.filter(
                vendor__name=vendor_name,
                sku=sku
            )

            if listing.exists():
                return redirect(listing.first().product)

            scrape = Scrape(vendor_name)
            product = scrape.scrape_by_url(sku)
            return redirect(product)

    messages.error(request, 'Sorry, couldn\'t find a matching product from your link. Please try again.')
    return redirect('/')
        
    