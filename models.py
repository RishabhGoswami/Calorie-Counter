from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django import forms
from django.core.exceptions import ValidationError

# Create your models here.
def validateh(Height):
    if(Height<20):
        raise forms.ValidationError('no')
class Profile(models.Model):
    Height=models.IntegerField(default=0,validators=[validateh])
    Weight=models.PositiveIntegerField(default=0)
    category = models.CharField(max_length=30)
    date=models.DateField(default=datetime.now,editable=True)
    target=models.IntegerField(null=True,default=0)
    sex=models.CharField(default='',max_length=6)
    age=models.IntegerField(default=0)
    user=models.CharField(max_length=20,default='')
    lifestyle=models.CharField(default='',max_length=20)
    objects=models.Manager()
    def __str__(self):
        return self.category
class Category(models.Model):
    name=models.CharField(max_length=25)
    description=models.TextField(default='')
    image=models.ImageField(upload_to='calorie/images',default='')
    objects=models.Manager()
    def __str__(self):
        return self.name
class life(models.Model):
    name=models.CharField(max_length=20)
    objects=models.Manager()
    def __str__(self):
        return self.name
class FoodAnalysis(models.Model):
    Name=models.CharField(max_length=40)
    Quantity=models.IntegerField()
    user=models.CharField(default='',max_length=40)
    calorie=models.FloatField(default=0)
    objects=models.Manager()
    def __str__(self):
        return self.Name