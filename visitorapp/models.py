from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    phone=models.CharField(max_length=100,default='')
    def __str__self(self):
        return self.user.username
def create_profile(sender,**kwargs):
    if kwargs['created']:
        user_profile=UserProfile.objects.create(user=kwargs['instance'])
post_save.connect(create_profile,sender=User)

class Visit(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    checkin=models.DateTimeField(auto_now=False)
    host_name=models.CharField(max_length=100,default='')
    host_email=models.CharField(max_length=100,default='')
    host_phone=models.CharField(max_length=100,default='')
    checkout=models.DateTimeField(auto_now=False)

    def __str__self(self):
        return self.host_name

def create_visit(sender,**kwargs):
    if kwargs['created']:
        user_visit=Visit.objects.create(user=kwargs['instance'])

class Host(models.Model):
    host_name=models.CharField(max_length=100,default='')
    host_email=models.CharField(max_length=100,default='')
    host_phone=models.CharField(max_length=100,default='')
    def __str__(self):
        return self.host_name
    