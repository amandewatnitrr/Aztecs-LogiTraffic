from django.shortcuts import render
from django.db.models import Q
from django.shortcuts import render

from User.models import UserExtended

from django.contrib.auth import (authenticate,
                                 login)

from rest_framework.response import Response

from rest_framework.filters import (SearchFilter,
                                     OrderingFilter)

from rest_framework.status import (HTTP_200_OK, 
                                   HTTP_400_BAD_REQUEST,
                                   HTTP_404_NOT_FOUND,
                                   HTTP_204_NO_CONTENT)

from rest_framework.views import APIView

from rest_framework.generics import (CreateAPIView ,
                                     ListAPIView,
                                     RetrieveAPIView,
                                     RetrieveUpdateAPIView,
                                     DestroyAPIView)

from Device.serializers import (DeviceCreateUpdateSerializer,
                                DeviceListSerializer,
                                DeviceDetailSerializer,
                                DeviceTheftSerialiser)

from rest_framework.permissions import (AllowAny,
                                        IsAuthenticated,
                                        IsAuthenticatedOrReadOnly,
                                        IsAdminUser)

from Device.permissions import IsOwner

from Device.models import Device

from django.contrib.auth import get_user_model

from LiveData.models import LiveData

from rest_framework.exceptions import APIException

User = get_user_model()            
# Create your views here.

class DeviceCreateAPIView(CreateAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceCreateUpdateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner = self.request.user)
        instance = serializer.save()
        LiveData.objects.create(device = instance)       


class DeviceUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceCreateUpdateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwner]

class DeviceListAPIView(ListAPIView):
    # queryset = Device.objects.all()
    serializer_class = DeviceListSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['is_theft', 'date_theft']

    
    def get_queryset(self, *args, **kwargs):
        queryset_list = Device.objects.all()
        query = self.request.GET.get('q')
        if query:
            queryset_list = queryset_list.filter(
                Q(is_theft__icontains = query)|
                Q(date_theft__icontains = query)
            ).distinct()
        return queryset_list       

class DeviceDetailAPIView(RetrieveAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceDetailSerializer
    permission_classes = [IsAuthenticated]

class DeviceTheftAPIView(RetrieveUpdateAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceTheftSerialiser
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwner]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.theft()
        instance.theft_at()

class DeviceRetrieveAPIView(RetrieveUpdateAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceTheftSerialiser
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwner]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.is_theft is True:
            instance.retrieved()
            instance.is_retrieved()
        else:
            raise APIException('To retrieve, vehicle must be stolen first')    
    
    