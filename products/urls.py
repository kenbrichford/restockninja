from django.urls import path, register_converter
from .views import ProductDetailView
from .converters import TagConvertor

register_converter(TagConvertor, 'tag')

urlpatterns = [
    path('<slug:slug>/<tag:tag>/', ProductDetailView.as_view(), name='product')
]