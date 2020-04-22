from django.views.generic import DetailView
from .models import Product

class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'product'
