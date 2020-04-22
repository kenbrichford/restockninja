from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.utils import timezone
from datetime import timedelta

# @shared_task
# def scrape(vendor_name, path=None):
#     if not path:
#         one_minute_ago = timezone.now() - timedelta(minutes=1)

#         listings = Listing.objects.filter(updated_time__lte=one_minute_ago, vendor__name=vendor_name)\
#             .order_by('updated_time')

#     if listings:
#         store = create_store(vendor_name)

#         truncated_listings = {i.sku: i for i in listings[:store.items_per_request]}

#         skus = ''.join([listing.sku for listing in listings[:store.items_per_request]])

#         url = store.create_sku_url(skus)
        
#         response = requests.get(url.endpoint, params=url.params)
        
#         items = store.get_items(response.json())
        
#         if items:
#             for item in items:
#                 parsed_data = store.parse_data(item)
                
#                 listing = truncated_listings.pop(parsed_data.sku)
                
#                 upload_data(listing, parsed_data)
        
#         else:
#             print('No items were returned from this request: %s' % response.text, flush=True)

#         for listing in list(truncated_listings.values()):
#             listing.save()
