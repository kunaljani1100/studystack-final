from django import forms
from django.contrib.auth.models import User
from basic_app.models import NewUserOTPVerification
from basic_app.models import OTPVerification
from basic_app.models import UserProfileInfoForm
from basic_app.models import Grp
from basic_app.models import GroupAssociation
from basic_app.models import Post
from basic_app.models import Comment

class UserForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model=User
        fields=('username','email','password')

class UserProfileInfoForm(forms.ModelForm):
    class Meta():
        model=UserProfileInfoForm
        fields=('first_name','last_name')

class GrpForm(forms.ModelForm):
    class Meta():
        model=Grp
        fields=('groupID','group_name')

class GroupAssociationForm(forms.ModelForm):
    class Meta():
        model=GroupAssociation
        fields=('username','groupID','group_name')

class PostForm(forms.ModelForm):
    class Meta():
        model=Post
        fields=('groupID','username','post_content','group_name')

class CommentForm(forms.ModelForm):
    class Meta():
        model=Comment
        fields=('groupID','username','post_content','group_name','comment')

'''
class NewUserOTPVerification(forms.ModelForm):
    class Meta():
        model=NewUserOTPVerification
        fields=('emailID','otp')

class OTPVerification(forms.ModelForm):
    class Meta():
        model=OTPVerification
        fields=('emailID','otp')
'''
