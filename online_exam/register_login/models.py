from django.db import models

# Create your models here.


class StudentDetails(models.Model):
    name = models.CharField(max_length=100,null=True,blank=True) 
    address = models.CharField(max_length=100,null=True,blank=True) 
    email = models.CharField(max_length=100,null=True,blank=True) 
    username = models.CharField(max_length=100,null=True,blank=True) 
    phone = models.CharField(max_length=100,null=True,blank=True) 
    password = models.CharField(max_length=100,null=True,blank=True) 
    image = models.ImageField(null=True,blank = True,upload_to = 'image') 


