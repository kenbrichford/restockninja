from datetime import timedelta
from django.utils import timezone
from django.views.generic import DetailView
from .models import Product, Image
from listings.models import Listing, Price
from scrape.scrape import Scrape
from alerts.models import Alert
from alerts.forms import AlertForm

class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'product'

    def get_object(self):
        obj = super().get_object()

        time_between_updates = timedelta(minutes=5)
        listings = Listing.objects.filter(
            updated_time__lte=(timezone.now() - time_between_updates),
            product=obj
        )

        for listing in listings:
            scrape = Scrape(listing.vendor.name)
            scrape.scrape_by_listing([listing])

        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['images'] = Image.objects.filter(product=context['product']).order_by('-primary')
        context['prices'] = Price.objects.filter(listing__product=context['product'])\
            .order_by('listing', '-updated_time').distinct('listing')
        alert = Alert(product=context['product'])
        context['alert_form'] = AlertForm(instance=alert)
        return context