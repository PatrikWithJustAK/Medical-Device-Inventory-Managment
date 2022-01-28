from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class ServiceCenter(models.Model):
    name =models.CharField("Name of the service center", max_length=50)
    state = models.CharField("State of this service center", max_length=50)
    street_address = models.CharField("Address of the service center", max_length=50)
    zip_code = models.CharField("Zip Code of this service center", max_length=50)
    manager = models.ForeignKey("Profiles.Profile", verbose_name="Which manager runs this store?", on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return str(self.name)