from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from Device.views import (DeviceCreateAPIView,
                         DeviceUpdateAPIView,
                         DeviceListAPIView,
                         DeviceDetailAPIView,
                         DeviceTheftAPIView,
                         DeviceRetrieveAPIView)

app_name = 'Device'

urlpatterns = [
    url(r'list/$', DeviceListAPIView.as_view(), name='list'),
    url(r'create/$', DeviceCreateAPIView.as_view(), name='create'),
    url(r'edit/(?P<pk>\d+)$', DeviceUpdateAPIView.as_view(), name='update'),    
    url(r'detail/(?P<pk>\d+)$', DeviceDetailAPIView.as_view(), name='detail'),
    url(r'theft/(?P<pk>\d+)$', DeviceTheftAPIView.as_view(), name='theft'),
    url(r'is_retrieved/(?P<pk>\d+)$', DeviceRetrieveAPIView.as_view(), name='retrieve'),
]
