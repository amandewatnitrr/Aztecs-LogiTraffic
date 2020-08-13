from rest_framework.serializers import (ModelSerializer,
                                         CharField,
                                         HyperlinkedIdentityField,
                                         SerializerMethodField,
                                         ValidationError)

from User.models import UserExtended

from Device.models import Device

from LiveData.serializer import LiveDataSerializer

from LiveData.models import LiveData

from django.contrib.auth import get_user_model
User = get_user_model() 

class DeviceCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = Device
        fields = [
            'number_plate',
            'car_image'
        ]

class DeviceListSerializer(ModelSerializer):
    detail_url = HyperlinkedIdentityField(view_name='device:detail', lookup_field = 'pk')
    class Meta:
        model = Device
        fields = [
            'pk',
            'number_plate',
            'is_theft',
            'date_theft',
            'detail_url'

        ]     

class DeviceDetailSerializer(ModelSerializer):
    edit_url = HyperlinkedIdentityField(view_name='device:update', lookup_field='pk')
    # delete_url = HyperlinkedIdentityField(view_name='user:delete', lookup_field='pk')
    username_owner = SerializerMethodField()
    car_image = SerializerMethodField()
    livedata = SerializerMethodField()
    class Meta:
        model = Device
        fields = [
            'pk',
            'owner',
            'car_image',
            'number_plate',
            'is_theft',
            'device_id',
            'date_theft',
            'username_owner',
            'edit_url',
            'livedata'
        ]     

    def get_username_owner(self, obj):
        return str(obj.owner.username)    

    def get_car_image(self, obj):
        return obj.car_image.url    

    def get_livedata(self, obj):
        d_qs = LiveData.objects.filter(device = obj)
        livedata = LiveDataSerializer(d_qs, many = True).data
        return livedata 
        
class DeviceTheftSerialiser(ModelSerializer):
    class Meta:
        model = Device
        fields = ['is_theft']        

class DeviceSerializer(ModelSerializer):
    # edit_url = HyperlinkedIdentityField(view_name='device:update', lookup_field='pk')
    # delete_url = HyperlinkedIdentityField(view_name='user:delete', lookup_field='pk')
    username_owner = SerializerMethodField()
    car_image = SerializerMethodField()
    # livedata = SerializerMethodField()
    class Meta:
        model = Device
        fields = [
            'pk',
            'owner',
            'car_image',
            'number_plate',
            'is_theft',
            'device_id',
            'date_theft',
            'username_owner',
        ]

    def get_username_owner(self, obj):
        return str(obj.owner.username)    

    def get_car_image(self, obj):
        return obj.car_image.url    
        