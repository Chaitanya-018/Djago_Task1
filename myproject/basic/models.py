from django.db import models

# Create your models here.

class StudentNew(models.Model):
    name=models.CharField(max_length=100)
    age=models.IntegerField()
    email=models.EmailField(unique=True)


# New model for your Post API task 08-11-2025
class InstaPost(models.Model):
    post_name = models.CharField(max_length=100)
    post_type = models.CharField(max_length=50)
    post_date = models.DateField()
    post_description = models.TextField()

#users login model 
class Users(models.Model):
    username=models.CharField(max_length=100,unique=True)
    email=models.EmailField(unique=True)
    password=models.CharField(max_length=100)   