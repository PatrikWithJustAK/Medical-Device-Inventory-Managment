import email
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user =models.ForeignKey(User, verbose_name="The User object associated with this profile", on_delete=models.CASCADE)
    home_center = models.ForeignKey("ServiceCenter.ServiceCenter", verbose_name="What location does this user work at?", on_delete=models.CASCADE, null=True)
    first_name = models.CharField("User's first name", max_length=50)
    last_name = models.CharField("User's last name", max_length=50, null=True, blank=True)
    email = models.EmailField("User's email", max_length=254, null =True, blank=True )

    def __str__(self):
        return str(self.user)
    
    def get_user(self):
        return self.user
    
    def get_center(self):
        return self.home_center

    
