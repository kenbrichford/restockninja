import re
from datetime import timedelta
from urllib.parse import unquote, urlparse
from django.utils import timezone
from django.shortcuts import render, redirect
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from products.models import Product
from listings.models import Listing
from scrape.scraper import Scraper

stores = [
    {'name': 'Walmart', 'domain': 'walmart', 'pattern': r'(?<=\/)\d{9}$'},
    {'name': 'Best Buy', 'domain': 'bestbuy', 'pattern': r'(?<=\/)\d{7}(?=(\.p)$)'},
    {'name': 'Target', 'domain': 'target', 'pattern': r'(?<=(\/A-))\d{8}$'}
]

def get_sku(pattern, url_path):
    try:
        sku = re.search(pattern, url_path).group(0)
    except AttributeError:
        sku = None
    
    return sku   

def search(request):
    query = request.GET.get('query', None)

    if query:
        validator = URLValidator()

        query = unquote(query)
        
        try:
            validator(query)

            url = urlparse(query)

            domain = url.netloc.split('.')[-2]

            store = next(store for store in stores if store.get('domain') == domain)

            vendor_name = store.get('name')
        
            sku = get_sku(store.get('pattern'), url.path)

            if vendor_name:
                one_hour_ago = timezone.now() - timedelta(minutes=1)

                listing = Listing.objects.filter(
                    updated_time__lte=one_hour_ago,
                    vendor__name=vendor_name,
                    sku=sku
                )

                if listing.exists():
                    return redirect(listing.first().product)

                scraper = Scraper(vendor_name)
                scraper.scrape('url', sku)
                return redirect(scraper.product)

            return render(request,'search/search.html',{})
        
        except ValidationError:
            pass
        
    