from django import forms
from products.models import Product
from .models import Alert, Email

class AlertForm(forms.ModelForm):
    FREQUENCIES = [
        (604800, 'Weekly'),
        (86400, 'Daily'),
        (43200, 'Two per day'),
        (28800, 'Three per day'),
        (3600, 'Hourly'),
        (0, 'All updates'),
    ]

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Enter valid email address'})
    )
    email_frequency = forms.ChoiceField(label='Frequency', choices=FREQUENCIES)
    product = forms.ModelChoiceField(
        queryset=Product.objects.all(),
        widget=forms.HiddenInput()
    )

    class Meta:
        model = Alert
        fields = ['email', 'email_frequency', 'product']

    def clean(self):
        if self.cleaned_data.get('email'):
            email_address = self.cleaned_data['email']
            email = Email.objects.get_or_create(address=email_address)[0]
            self.cleaned_data['email'] = email
        return super().clean()
    