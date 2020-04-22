from urllib.parse import unquote, urlparse 
from django.shortcuts import render, redirect
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from products.models import Product
from scrape.scraper import scrape_search

def search(request):
    query = request.GET.get('query', None)

    if query:
        validator = URLValidator()

        query = unquote(query)
        
        try:
            validator(query)
            
            product = scrape_search(urlparse(query))

            if product:
                return redirect(product)
            else:
                return render(request,'search/search.html',{})
        
        except ValidationError:
            pass
        
    