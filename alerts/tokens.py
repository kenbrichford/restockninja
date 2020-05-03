from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six

class AlertConfirmationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, alert, timestamp):
        return (
            six.text_type(alert.pk) + six.text_type(timestamp) +
            six.text_type(alert.is_confirmed)
        )

alert_confirmation_token = AlertConfirmationTokenGenerator()