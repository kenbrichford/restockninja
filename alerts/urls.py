from django.urls import path, re_path
from .views import create_alert, confirm_alert, delete_alert, delete_email

urlpatterns = [
    path('new/', create_alert, name='create-alert'),
    re_path(r'^confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', confirm_alert, name='confirm-alert'),
    re_path(r'^delete/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', delete_alert, name='delete-alert'),
    re_path(r'^delete-all/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', delete_email, name='delete-email'),
]