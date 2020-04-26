from django import forms
from mptt.forms import TreeNodeChoiceField
from .models import Product, Category

class ProductForm(forms.ModelForm):
    category = TreeNodeChoiceField(queryset=Category.objects.all())

    class Meta:
        model = Product
        fields = ('category', 'brand', 'name', 'featured')