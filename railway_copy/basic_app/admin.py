from django.contrib import admin
from basic_app.models import UserProfileInfoForm
from basic_app.models import OTPVerification
from basic_app.models import NewUserOTPVerification
from basic_app.models import Grp
from basic_app.models import GroupAssociation
from basic_app.models import Post
from basic_app.models import Comment
# Register your models here.
admin.site.register(UserProfileInfoForm)
admin.site.register(OTPVerification)
admin.site.register(NewUserOTPVerification)
admin.site.register(Grp)
admin.site.register(GroupAssociation)
admin.site.register(Post)
admin.site.register(Comment)
