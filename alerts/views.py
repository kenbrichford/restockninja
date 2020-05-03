from django.core.mail import send_mail
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from products.models import Product
from .models import Alert, Email
from .forms import AlertForm
from .tokens import alert_confirmation_token

def send_confirmation_email(request, product, alert):
    subject = 'Confirm your alert for %s on Restock Ninja' % product.name
    message = render_to_string('alerts/alert_confirmation_email.html', {
        'domain': request.META['HTTP_HOST'],
        'product': product,
        'uid': urlsafe_base64_encode(force_bytes(alert.pk)),
        'token': alert_confirmation_token.make_token(alert)
    })
    send_mail(
        subject,
        message,
        'alerts@restock.ninja',
        [alert.email.address],
        fail_silently=False
    )

def create_alert(request):
    if request.method == 'POST':
        alert_form = AlertForm(request.POST)
        
        if alert_form.is_valid():
            product = alert_form.cleaned_data['product']

            alert, created = Alert.objects.update_or_create(
                email = alert_form.cleaned_data['email'],
                product = product,
                defaults = {'verify': alert_form.cleaned_data['verify']}
            )

            if not alert.is_confirmed:
                send_confirmation_email(request, product, alert)
            
            if created:
                messages.success(request, 'Great success! We\'ve sent you an email to confirm your brand new alert.')
            else:
                messages.info(request, 'Looks like you were already in the system, but we\'ve updated your request.')
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
