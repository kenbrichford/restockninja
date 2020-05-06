from datetime import timedelta
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .models import Alert
from .tokens import alert_confirmation_token, alert_delete_token, email_delete_token

def send_alert_email(subject, message, alert):
    send_mail(
        subject,
        message,
        'alerts@restock.ninja',
        [alert.email.address],
        fail_silently=False
    )

def send_update_email(alert, price):
    subject = '%s is back in stock!' % alert.product.name
    message = render_to_string('alerts/alert_update_email.html', {
        'domain': 'https://restock.ninja',
        'product': alert.product,
        'vendor': price.listing.vendor.name,
        'alert_uid': urlsafe_base64_encode(force_bytes(alert.pk)),
        'alert_token': alert_delete_token.make_token(alert),
        'email_uid': urlsafe_base64_encode(force_bytes(alert.email.pk)),
        'email_token': email_delete_token.make_token(alert.email)
    })
    send_alert_email(subject, message, alert)

    
def send_confirmation_email(alert):
    subject = 'Confirm your alert for %s on Restock Ninja' % alert.product.name
    message = render_to_string('alerts/alert_confirmation_email.html', {
        'domain': 'https://restock.ninja',
        'product': alert.product,
        'uid': urlsafe_base64_encode(force_bytes(alert.pk)),
        'token': alert_confirmation_token.make_token(alert),
    })
    send_alert_email(subject, message, alert)

def send_alerts(price):
    alerts = Alert.objects.filter(product=price.listing.product, is_confirmed=True)
        
    for alert in alerts:
        if alert.last_notified:
            email_frequency = timedelta(seconds=alert.email_frequency)
            time_since_notified = timezone.now() - alert.last_notified
            if time_since_notified < email_frequency:
                continue
        send_update_email(alert, price)
        alert.last_notified = timezone.now()
        alert.save()
