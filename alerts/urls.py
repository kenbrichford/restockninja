from django.urls import path, re_path
from .views import create_alert, confirm_alert

urlpatterns = [
    path('new/', create_alert, name='create_alert'),
    re_path(r'^confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', confirm_alert, name='confirm_alert')
]