from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.template.loader import render_to_string
from products.models import Product
from .models import Alert, Email
from .forms import AlertForm
from .tokens import alert_confirmation_token, alert_delete_token, email_delete_token
from .alert import send_confirmation_email

def create_alert(request):
    if request.method == 'POST':
        alert_form = AlertForm(request.POST)
        
        if alert_form.is_valid():
            product = alert_form.cleaned_data['product']

            alert, created = Alert.objects.update_or_create(
                email = alert_form.cleaned_data['email'],
                product = product,
                defaults={
                    'email_frequency': alert_form.cleaned_data['email_frequency']
                }
            )

            if not alert.is_confirmed:
                send_confirmation_email(alert)
            
            if created:
                messages.success(request, 'Great success! We\'ve sent you an email to confirm your brand new alert.')
            else:
                messages.info(request, 'Your alert has been updated. We\'ll be in touch as soon as your item is available.')
        else:
            product = Product.objects.get(pk=alert_form.data.get('product'))
            messages.error(request, 'It seems there was an error with your entry. Please try again.')
    return redirect(product)

def confirm_alert(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        alert = Alert.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Alert.DoesNotExist):
        alert = None

    if alert and alert_confirmation_token.check_token(alert, token):
        alert.is_confirmed = True
        alert.save()
        messages.success(request, 'Congrats! You will be notified the next time your product is available.')
    else:
        messages.error(request, 'Sorry, there was an error confirming your alert. Please try again.')

    return redirect('/')

def delete_alert(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        alert = Alert.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Alert.DoesNotExist):
        alert = None
    
    if request.method == 'POST':
        if alert and alert_delete_token.check_token(alert, token):
            alert.delete()
            messages.success(request, 'You have successfully unsubscribed from this alert.')
        else:
            messages.error(request, 'Sorry, there was an error with your request. Please try again.')

        return redirect('/')
    return render(request, 'alerts/alert_confirm_delete.html', {'alert': alert})
    

def delete_email(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        email = Email.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Email.DoesNotExist):
        email = None

    if request.method == 'POST':
        if email and email_delete_token.check_token(email, token):
            email.delete()
            messages.success(request, 'You have successfully unsubscribed from all alerts.')
        else:
            messages.error(request, 'Sorry, there was an error with your request. Please try again.')

        return redirect('/')
    return render(request, 'alerts/email_confirm_delete.html')
