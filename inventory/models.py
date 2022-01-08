from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django_prometheus.models import ExportModelOperationsMixin
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class ComponentMeasurementUnit(ExportModelOperationsMixin('ComponentMeasurementUnit'), models.Model):
    unit_name = models.CharField(max_length=10)
    unit_description = models.CharField(max_length=200,null=True, blank=True)

    def __str__(self):
        return self.unit_name


class Building(ExportModelOperationsMixin('Building'), models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200,null=True, blank=True)
    postcode = models.CharField(max_length=20,null=True,blank=True)

    def __str__(self):
        return self.name


class Room(ExportModelOperationsMixin('Room'), models.Model):
    name = models.CharField(max_length=200)
    short_code = models.CharField(max_length=5,null=True,blank=True)
    building = models.ForeignKey(Building, on_delete=models.CASCADE)

    def __str__(self):
        return self.name



class StorageUnit(ExportModelOperationsMixin('StorageUnit'), models.Model):
    name = models.CharField(max_length=200)
    short_code = models.CharField(max_length=5,null=True,blank=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class StorageBin(ExportModelOperationsMixin('StorageBin'), models.Model):
    name = models.CharField(max_length=200)
    short_code = models.CharField(max_length=5,null=True,blank=True)
    unit_row = models.CharField(max_length=5,null=True,blank=True)
    unit_column = models.CharField(max_length=5,null=True,blank=True)
    storage_unit = models.ForeignKey(StorageUnit, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Component(ExportModelOperationsMixin('Component'), models.Model):
    name = models.CharField(max_length=200)
    sku = models.CharField(max_length=100)
    mpn = models.CharField(max_length=100, null=True, blank=True)
    upc = models.IntegerField(null=True, blank=True)
    storage_bin = models.ManyToManyField(StorageBin)
    measurement_unit = models.ForeignKey(ComponentMeasurementUnit, on_delete=models.CASCADE)
    qty = models.IntegerField(default=0, validators=[MinValueValidator(0)])

    def __str__(self):
        return self.name


#### Membership Models
class MembershipLevel(models.Model):
    name = models.CharField(max_length=200)
    monthly_fee = models.IntegerField(null=False, blank=False, default=10)

    def __str__(self):
        return self.name

class MemberMembershipLevel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    membership_level = models.ForeignKey(MembershipLevel, on_delete=models.CASCADE)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        MemberMembershipLevel.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
    instance.membermembershiplevel.save()
