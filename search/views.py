import re
from urllib.parse import urlparse
from multiprocessing import Process, Queue
from django.contrib import messages
from django.contrib.postgres.search import SearchQuery, SearchVector
from django.shortcuts import render, redirect
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from products.models import Product
from listings.models import Listing
from scrape.scrape import Scrape

stores = [
    {'name': 'Walmart', 'domain': 'walmart', 'pattern': r'(?<=\/)\d{8,9}$'},
    {'name': 'Target', 'domain': 'target', 'pattern': r'(?<=(\/A-))\d{8}$'},
    {'name': 'Best Buy', 'domain': 'bestbuy', 'pattern': r'(?<=\/)\d{7}(?=(\.p)$)'},
]

def get_sku(pattern, url_path):
    try:
        return re.search(pattern, url_path).group(0)
    except AttributeError:
        return None

def search(request):
    query = request.GET.get('query')
    store = request.GET.get('store')
    sku = request.GET.get('sku')

    if store and store.strip() and sku and sku.strip():
        store = store.strip()
        sku = sku.strip()

        listing = Listing.objects.filter(vendor__name=store, sku=sku)

        if listing.exists():
            return redirect(listing.first().product)

        scrape = Scrape(store)
        return redirect(scrape.scrape_by_url(sku))

    if query and query.strip():
        query = query.strip()
        validate = URLValidator()

        try:
            validate(query)
            url = urlparse(query)
        except ValidationError:
            url = None
            
        if url:
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
                    if product:
                        return redirect(product)
            
            messages.error(request, 'Sorry, we couldn\'t find a matching product from your link. Please try again.')
            return redirect('/')
        
        else:
            products = Product.objects.annotate(search=SearchVector('name'))\
                .filter(search=SearchQuery(query))[:10]

            results = {}
            queue = Queue()
            for store in stores:
                scrape = Scrape(store.get('name'))
                Process(target=scrape.scrape_by_keyword, args=(query, queue)).start()
                results[store.get('name')] = queue.get()

            return render(request, 'search/search.html', {'products': products, 'results': results})
    
    return redirect('/')
    