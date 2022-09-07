from django.db import models

# Create your models here.


class User_details(models.Model):
    user_id = models.AutoField(primary_key=True)
    ip_add = models.CharField(max_length=30)
    download_link = models.CharField(max_length=255)
    location = models.CharField(max_length=255, null=True)
