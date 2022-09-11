from django.db import models

# Create your models here.


class User_details(models.Model):
    user_id = models.AutoField(primary_key=True)
    ip_add = models.CharField(max_length=30)
    download_link = models.CharField(max_length=255)
    location = models.CharField(max_length=255, null=True)
    download_type = models.CharField(max_length=30, null=True)


class Admins(models.Model):
    id = models.AutoField(primary_key=True)
    admin_name = models.CharField(max_length=50)
    admin_user_id = models.CharField(max_length=50)
    admin_password = models.CharField(max_length=50)
