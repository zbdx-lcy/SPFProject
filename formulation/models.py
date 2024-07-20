from django.db import models


# Create your models here.
# 配方表，如果有新配方添加，依次编号，不做新旧区分。
class formulations(models.Model):
    formulation_id = models.IntegerField(primary_key=True)
    formulation_name = models.CharField(max_length=10)
    pbt = models.FloatField(default=0)
    tdi = models.FloatField(default=0)
    tri_bis = models.FloatField(default=0)
    athree = models.FloatField(default=0)
    bonding_agent = models.FloatField(default=0)
    ap_small = models.FloatField(default=0)
    ap_large = models.FloatField(default=0)
    ai_powder = models.FloatField(default=0)
    tmp = models.FloatField(default=0)
    die_gly = models.FloatField(default=0)
    tri_glycol = models.FloatField(default=0)
    add_tdi = models.FloatField(default=0)

    def __unicode__(self):
        return str(self.formulation_id) + self.formulation_name

# class new_formulations(models.Model):
#     formulation_n_id = models.IntegerField(primary_key=True)
#     pbt = models.FloatField(default=0)
#     tdi = models.FloatField(default=0)
#     tri_bis = models.FloatField(default=0)
#     athree = models.FloatField(default=0)
#     bonding_agent = models.FloatField(default=0)
#     ap_small = models.FloatField(default=0)
#     ap_large = models.FloatField(default=0)
#     ai_powder = models.FloatField(default=0)
#     tmp = models.FloatField(default=0)
#     die_gly = models.FloatField(default=0)
#     tri_glycol = models.FloatField(default=0)
#     add_tdi = models.FloatField(default=0)
