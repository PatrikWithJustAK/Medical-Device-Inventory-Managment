from django.db.models.signals import post_save, pre_save
from .models import Profile
from django.contrib.auth.models import User 

def user_profile(sender, instance, created, **kwargs):
    if created: 
        Profile.objects.create(
            user=instance,
            first_name = instance.username,
            last_name = instance.last_name,
            email = instance.email
        )
        print('Profile Created!')
        print(instance)
post_save.connect(user_profile, sender=User)