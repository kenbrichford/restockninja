import threading
from datetime import timedelta
from django.utils import timezone
from django.views.generic import DetailView
from .models import Product, Image
from listings.models import Listing, Price
from scrape.scrape import Scrape

class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'product'
    slug_field = 'tag'

    def get_object(self):
        obj = super().get_object()

        time_between_updates = timedelta(minutes=5)
        listings = Listing.objects.filter(
            updated_time__lte=(timezone.now() - time_between_updates),
            product=obj
        )

        jobs = []
        for listing in listings:
            scrape = Scrape(listing.vendor.name)
            jobs.append(threading.Thread(target=scrape.scrape_by_listing, args=(listing,)))
        
        for job in jobs:
            job.start()
        
        for job in jobs:
            job.join()

        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['images'] = Image.objects.filter(product=context['product'])
        context['prices'] = Price.objects.filter(listing__product=context['product'])\
            .order_by('listing', '-updated_time').distinct('listing')
        return context