from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfileInfoForm(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,)
    first_name=models.CharField(max_length=300,blank=False)
    last_name=models.CharField(max_length=300,blank=False)
    active=models.CharField(max_length=5,blank=False)
    def __str__(self):
        return self.user.username
    # portfolio_site=models.URLField(blank=True)
    #
    # profile_pic=models.ImageField(upload_to='profile_pics',blank=True)

class NewUserOTPVerification(models.Model):
    email=models.CharField(max_length=300,blank=False)
    otp=models.CharField(max_length=4)
    def __str__(self):
        return self.email
    # portfolio_site=models.URLField(blank=True)
    #
    # profile_pic=models.ImageField(upload_to='profile_pics',blank=True

class OTPVerification(models.Model):
    emailID=models.CharField(max_length=100,unique=True)
    otp=models.CharField(max_length=4)
    def __str__(self):
        return self.emailID

class Grp(models.Model):
    groupID=models.CharField(max_length=100)
    group_name=models.CharField(max_length=100)
    def __str__(self):
        return self.groupID

class GroupAssociation(models.Model):
    username=models.CharField(max_length=100)
    groupID=models.CharField(max_length=100)
    group_name=models.CharField(max_length=100)
    isAdmin=models.CharField(max_length=100)
    def __str__(self):
        return self.groupID

class Post(models.Model):
    groupID=models.CharField(max_length=100)
    username=models.CharField(max_length=100)
    group_name=models.CharField(max_length=100)
    post_content=models.TextField(max_length=None)
    def __str__(self):
        return self.groupID

class Comment(models.Model):
    groupID=models.CharField(max_length=100)
    username=models.CharField(max_length=100)
    group_name=models.CharField(max_length=100)
    post_content=models.TextField(max_length=None)
    comment=models.TextField(max_length=None)
    def __str__(self):
        return self.groupID
