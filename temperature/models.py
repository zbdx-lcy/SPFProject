from django.db import models


# Create your models here.
class temperature(models.Model):
    temp_id = models.IntegerField(primary_key=True)
    temp_value = models.IntegerField(default=0)
