from django import forms
from products.models import Product
from .models import Alert, Email

class AlertForm(forms.ModelForm):
    email = forms.EmailField()
    product = forms.ModelChoiceField(
        queryset=Product.objects.all(),
        widget=forms.HiddenInput()
    )

    class Meta:
        model = Alert
        fields = ['email', 'verify', 'product']

    def clean(self):
        if self.cleaned_data.get('email'):
            email_address = self.cleaned_data['email']
            email = Email.objects.get_or_create(address=email_address)[0]
            self.cleaned_data['email'] = email
        return super().clean()
    