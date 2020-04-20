from django import forms
from mptt.forms import TreeNodeChoiceField
from .models import Product, Category

class ProductForm(forms.ModelForm):
    tag = forms.CharField(required=False)
    category = TreeNodeChoiceField(queryset=Category.objects.all())

    class Meta:
        model = Product
        fields = ('category', 'manufacturer', 'name', 'featured')