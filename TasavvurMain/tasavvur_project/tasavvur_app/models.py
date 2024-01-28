from django.db import models


class DataSets(models.Model):
    title = models.CharField(max_length=250)
    data_id = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    file = models.FileField(upload_to='datasets/')
    file_l = models.URLField()
