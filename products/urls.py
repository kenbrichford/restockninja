from django.urls import re_path, register_converter
from .views import ProductDetailView

urlpatterns = [
    re_path(r'^([\w-]+)/(?P<pk>[A-Z0-9]{7})/$', ProductDetailView.as_view(), name='product-detail')
]