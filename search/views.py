from urllib.parse import unquote, urlparse 
from django.shortcuts import render
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from products.models import Product
from listings.models import Vendor
from scrape.tasks import single_scrape

def get_domain(url):
    vendor_names = Vendor.objects.values_list('name', flat=True)

    name_list = [i for i in vendor_names if ''.join(i.lower()) in url.netloc.split('.')]

    vendor_name = name_list[0] if len(name_list) > 0 else None

    return vendor_name

def search(request):
    query = request.GET.get('query', None)

    if query:
        validator = URLValidator()

        query = unquote(query)
        
        try:
            validator(query)
            
            url = urlparse(query)
            
            vendor_name = get_domain(url)

            if vendor_name:
                single_scrape(vendor_name, url.path)

            return render(
                request,
                'search/search.html',
                {
                    'query': url,
                    'vendor': vendor_name,
                }
            )
        
        except ValidationError:
            pass
        
    