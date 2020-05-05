from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from listings.models import Listing
from scrape.scrape import Scrape

@shared_task
def scrape_for_alerts(vendor_name):
    time_between_updates = timedelta(minutes=5)
    listings = Listing.objects.filter(
        updated_time__lte=(timezone.now() - time_between_updates),
        vendor__name=vendor_name,
        product__total_alerts__gt=0
    ).order_by('-product__total_alerts', 'updated_time')

    if listings:
        scrape = Scrape(vendor_name)
        scrape.scrape_by_listing(listings)
