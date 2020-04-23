from django.views.generic import DetailView
from .models import Product, Image
from listings.models import Price

class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'product'
    slug_field = 'tag'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['images'] = Image.objects.filter(product=context['product'])
        context['prices'] = Price.objects.filter(listing__product=context['product'])\
            .order_by('listing', '-updated_time').distinct('listing')
        return context