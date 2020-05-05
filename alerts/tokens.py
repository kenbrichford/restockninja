from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six

class AlertConfirmationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, alert, timestamp):
        return (
            six.text_type(alert.pk) + six.text_type(timestamp) +
            six.text_type(alert.is_confirmed)
        )

class AlertDeleteTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, alert, timestamp):
        return (
            six.text_type(alert.pk) + six.text_type(timestamp)
        )

class EmailDeleteTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, email, timestamp):
        return (
            six.text_type(email.pk) + six.text_type(timestamp)
        )

alert_confirmation_token = AlertConfirmationTokenGenerator()
alert_delete_token = AlertDeleteTokenGenerator()
email_delete_token = EmailDeleteTokenGenerator()
