from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from User.models import UserExtended
User = get_user_model()
# Create your models here.
class Device(models.Model):
    owner = models.ForeignKey(User, related_name='owner', on_delete = models.CASCADE)
    number_plate = models.CharField(max_length=10, blank=False)
    car_image = models.ImageField(upload_to = 'CarImage', blank=False)
    is_theft = models.BooleanField(default=False)
    device_id = models.CharField(max_length=20, default='Pass')
    date_theft = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.owner.username

    def theft(self):
        self.is_theft = True
        self.save()    

    def theft_at(self):
        self.date_theft = timezone.now()
        self.save()

    def retrieved(self):
        self.date_theft = None
        self.save()

    
    def is_retrieved(self):
        self.is_theft = False
        self.save()  