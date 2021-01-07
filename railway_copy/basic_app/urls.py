from django.conf.urls import url
from basic_app import views

#TEMPLATE URLS!
app_name='basic_app'
urlpatterns=[
    url(r'^register/$',views.register,name='register'),
    url(r'^user_login/',views.user_login,name='user_login'),
    url(r'^account_recovery/',views.account_recovery,name='account_recovery'),
    url(r'^otp_verification/',views.otp_verification,name='otp_verification'),
    url(r'^result/',views.result,name='result'),
    url(r'^new_user_otp_verification/',views.new_user_otp_verification,name='new_user_otp_verification'),
    url(r'^change_password/',views.change_password,name='change_password'),
    url(r'^quiz/',views.quiz,name='quiz'),
    url(r'^load_quiz/',views.load_quiz,name='load_quiz'),
    url(r'^add_member/',views.add_member,name='add_member'),
    url(r'^view_members_in_groups/',views.view_members_in_groups,name='view_members_in_groups'),
    url(r'^add_post/',views.add_post,name='add_post'),
    url(r'^view_posts/',views.view_posts,name='view_posts'),
    url(r'^add_comment/',views.add_comment,name='add_comment'),
    url(r'^delete_user_from_group/',views.delete_user_from_group,name='delete_user_from_group'),
    url(r'^delete_group/',views.delete_group,name='delete_group'),
]
