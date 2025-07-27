from django.db import models

class Userdata(models.Model):
    first_name = models.CharField(max_length=100, default="Unknown")
    last_name = models.CharField(max_length=100, default="Unknown")
    address = models.CharField(max_length=200, default="Unknown")
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    phone = models.IntegerField(default=0000000000)
    password = models.CharField(max_length=14)
    
    def __str__(self):
        return self.username