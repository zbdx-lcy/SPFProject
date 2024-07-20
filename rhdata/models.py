from django.db import models

from formulation.models import formulations
from temperature.models import temperature


# Create your models here.
class rheological_data(models.Model):
    rh_id = models.AutoField(primary_key=True)
    formulation_id = models.ForeignKey(formulations, on_delete=models.CASCADE)
    temperature_id = models.ForeignKey(temperature, on_delete=models.CASCADE)
    temp_mark = models.IntegerField()
    time_min = models.FloatField()
    time_s = models.FloatField()
    temp = models.FloatField()
    energy_storage_mod = models.FloatField()
    loss_mod = models.FloatField()
    loss_factor = models.FloatField()
    complex_viscosity = models.FloatField()
    clearances = models.FloatField()
    normal_force = models.FloatField()
    torsion = models.FloatField()
    state_mark = models.CharField(max_length=50)
