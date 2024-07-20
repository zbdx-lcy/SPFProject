from django.db import models


# Create your models here.
class FileContent(models.Model):
    title = models.CharField('文件名称', max_length=20)
    files = models.FileField(upload_to='files')
