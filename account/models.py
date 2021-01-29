from djongo import models

# Create your models here.
class User(models.Model):
    _id = models.ObjectIdField()
    name = models.CharField(max_length=20,blank=False)
    email = models.EmailField(max_length=256, blank=False, unique=True)
    contact = models.BigIntegerField(blank=False,unique=True)
    password = models.CharField(max_length=300)
