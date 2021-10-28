from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class AppUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employee_email = models.CharField(max_length=50)

    def __str__(self) -> str:
        return str(self.user)



class Property(models.Model):
    property_name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    lat = models.IntegerField(default=0, validators=[MinValueValidator(-90), MaxValueValidator(90)])
    lon = models.IntegerField(default=0, validators=[MinValueValidator(-180), MaxValueValidator(180)])

    def __str__(self):
        return str(self.property_name)



class Scan(models.Model):
    user = models.ForeignKey(AppUser, related_name="appuser", on_delete=models.CASCADE, default=1)
    property = models.ForeignKey(Property, related_name="property", on_delete=models.CASCADE, default=1)
    image = models.ImageField(upload_to="scan_photos")
    raw_text = models.TextField(default="")
    scan_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "{}: {}".format(str(self.scan_date), str(self.property))