from django.shortcuts import render
from basic_app.forms import UserForm,UserProfileInfoForm
from basic_app.forms import User
from basic_app.forms import NewUserOTPVerification
from basic_app.forms import OTPVerification
from basic_app.forms import Grp
from basic_app.forms import GroupAssociation
from basic_app.forms import Post
from basic_app.forms import Comment
# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

import random

groupID_filter=-1

#We view all the stations in the form of a table
#micah was here, this is just a test of Git and GitHub
def index(request):
    return render(request,'basic_app/index.html')

@login_required
def special(request):
    return HttpResponse("You are logged in, nice")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def new_user_otp_verification(request):

    #Receive the entered email, and the OTP from the user.
    entered_email=request.POST.get('emailID')
    entered_otp=request.POST.get('otp')

    #Encrypt the OPT using hashing so that it is not recoverable by the attacker
    encrypted_otp=encrypt_string(entered_otp)

    #Load the instances from the OTPVerification table which stores the email id and the hashed OTP.
    instances=OTPVerification.objects.order_by('emailID')

    #We iterate through all the OTP objects stored in the SQL table.
    for instance in instances:

        #We check the entries where the entered email ID and the email ID in the table are the same.
        if(entered_email==instance.emailID):

            #If the entered hash and the stored hash values are equal, then the verification is successful.
            if(encrypted_otp==instance.otp):
                OTPVerification.objects.filter(emailID=entered_email).delete()
                my_dict={'insert_error':'OTP verification successful!!!! Your account has been created.'}
                return render(request,'basic_app/result.html',context=my_dict)

            #If the entered hash and the stored hash are not equal, then the verification has failed.
            else:
                print('OTP verification failed!!!')
                my_dict={'insert_error':'OTP verification failed!!!!'}
                OTPVerification.objects.filter(emailID=entered_email).delete()
                return render(request,'basic_app/result.html',context=my_dict)

        #The verification also fails when the email id entered does not exist.
        else:
            my_dict={'insert_error':'This email does not exist.'}
            OTPVerification.objects.filter(emailID=entered_email).delete()
            return render(request,'basic_app/result.html',context=my_dict)

def register(request):

    #Initally, the value of registered is false.
    registered=False
    if(request.method=='POST'):

        #We recieve the registration details from the user.
        user_form=UserForm(data=request.POST)
        profile_form=UserProfileInfoForm(data=request.POST)

        #We ensure that both the forms are valid, and them only we will proceed.
        if user_form.is_valid() and profile_form.is_valid():
            user=user_form.save()

            #An OTP verification is generated.
            new_otp_verification=NewUserOTPVerification()
            new_otp_verification.email=user.email
            temp_otp=''

            #The OTP consists of 4 digits randomly generated from 0 to 10.
            for i in range(4):
                temp_otp+=str(int(10*random.random()))

            #An automated email is sent from the account ilovedream75@gmail.com consisting of the OTP.
            from django.core.mail import send_mail
            send_mail('Recovery for Account With EmailID '+user.email,'OTP to verify account is:'+temp_otp,'ilovedream75@gmail.com',[user.email],fail_silently=False,)
            new_otp_verification.otp=encrypt_string(temp_otp)
            new_otp_verification.save()
            user.set_password(user.password)
            user.save()

            #We finally store the user registration details in an inactive state.

            profile=profile_form.save(commit=False)
            profile.user=user
            profile.active='False'

            profile.save()
            register=True
            my_dict={'email':user.email}
            return render(request,'basic_app/new_user_otp_verification.html',context=my_dict)
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form=UserForm()
        profile_form=UserProfileInfoForm()
    return render(request,'basic_app/registration.html',{'user_form':user_form,'profile_form':profile_form,'registered':registered})

def user_login(request):
    if request.method=="POST":

        #Accept the username and password from the user.
        username=request.POST.get('username')
        password=request.POST.get('password')

        #We use an inbuilt function to authenticate the user credentials.
        user=authenticate(username=username,password=password)

        #If the credentials are true, then the user is allowed to login.
        if user:

            #If the OTP verification has already been done successfully before.
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))

            #This is the case where the OTP verification has not been done successfully before.
            else:
                return HttpResponse("ACCOUNT NOT ACTIVE")

        #Otherwise the user is not allowed to login if the authenticate function returns a false value.
        else:
            print("Someone tried to login and failed!")
            print('Username: {} and {} password:'.format(username,password))
            my_dict={'insert_me':"Invalid username or password"}
            return render(request,'basic_app/login.html',context=my_dict)

    else:
        return render(request,'basic_app/login.html',{})

def account_recovery(request):

    #In case the user forgets his or her password, the system accepts the email ID of the user.
    emailID=request.POST.get('emailID')
    email_list=User.objects.order_by('email')
    print(email_list)
    print(emailID)
    emailfound=False

    #We will check if the mail exists in the list of mails or not.
    for mail in email_list:
        if(emailID==mail.email):
            emailfound=True
            break

    #If the email exists in the database, then an email is sent to the user with a generated OTP
    if(emailfound==True):
        from django.core.mail import send_mail
        otp=''
        for i in range(4):
            otp+=str(int(10*random.random()))
        send_mail('Recovery for Account With EmailID '+emailID,'OTP to verify account is:'+otp,'ilovedream75@gmail.com',[emailID],fail_silently=False,)
        otp_verify=OTPVerification()
        otp_verify.emailID=emailID
        otp_verify.otp=encrypt_string(otp)
        otp_verify.save()
        my_dict={'email':emailID}
        return render(request,'basic_app/otp_verification.html',context=my_dict)
    else:
        my_dict={'insert_error':'EmailID does not exist.'}
        return render(request,'basic_app/account_recovery.html',context=my_dict)

#Function for encryption of OTP using the sha256 algotithm
def encrypt_string(hash_string):
    import hashlib
    sha_signature = \
        hashlib.sha256(hash_string.encode()).hexdigest()
    return sha_signature

#Method to verify OTP
def otp_verification(request):

    #The email and the OTP are accepted from the user, and the OTP is encrypted.
    entered_email=request.POST.get('emailID')
    entered_otp=request.POST.get('otp')
    encrypted_otp=encrypt_string(entered_otp)
    instances=OTPVerification.objects.order_by('emailID')

    #Now we look at all the OTP instances in the table.
    for instance in instances:

        #We check of the entered email and the instance email match each other.
        if(entered_email==instance.emailID):

            #If the generated OTP and the entered OTP hash values both match each other, then a new password is generated.
            if(encrypted_otp==instance.otp):

                #The new password consists of 10 digits where each digit is randomly generated.
                new_password=''
                for i in range(10):
                    new_password+=str(int(10*random.random()))

                #The newly generated password is sent to the user.
                from django.core.mail import send_mail
                send_mail('New password','New Password is:'+new_password,'ilovedream75@gmail.com',[entered_email],fail_silently=False,)
                users=User.objects.order_by('email')

                #We iterate through the set of users, change the password and save the user credentials.
                for user in users:
                    if(user.email==entered_email):
                        user.password=new_password
                        user.set_password(user.password)
                        user.save()
                        break

            #Otherwise, we return a message stating that the OTP verification method has failed.
            else:
                print('OTP verification failed!!!')
                my_dict={'insert_error':'OTP verification failed!!!!'}
                OTPVerification.objects.filter(emailID=entered_email).delete()
                return render(request,'basic_app/result.html',context=my_dict)
        else:
            my_dict={'insert_error':'This email does not exist.'}
            OTPVerification.objects.filter(emailID=entered_email).delete()
            return render(request,'basic_app/result.html',context=my_dict)
    OTPVerification.objects.filter(emailID=entered_email).delete()
    my_dict={'insert_error':'OTP verification successful!!!! If you opted for account recovery, please check your email for the new password.'}
    return render(request,'basic_app/result.html',context=my_dict)

def result(request):
    return render(request,'basic_app/result.html',{})

def change_password(request):

    #We accept the original password, the new password and the confirmed new password.
    old_password=request.POST.get('old_password')
    new_password=request.POST.get('new_password')
    confirm_new_password=request.POST.get('confirm_new_password')
    current_user=request.user

    #We authenticate the user credintials which consist of the old and new password.
    cur_user=authenticate(username=current_user.username,password=old_password)
    if cur_user:

        #If the credentials are true, we will check if the new password and the confirmed new password match each other or not.
        if(new_password!='' and confirm_new_password!=''):
            if(new_password==confirm_new_password):
                current_user.password=new_password
                current_user.set_password(current_user.password)
                current_user.save()
                my_dict={'insert_error':'Password change successful.'}
                return render(request,'basic_app/result.html',context=my_dict)
    my_dict={'insert_me':'Password change failed.'}
    return render(request,'basic_app/change_password.html',context=my_dict)

def quiz(request):
    instances=Grp.objects.order_by('groupID')
    groupID=len(instances)+1
    group_name=request.POST.get('group_name')
    group=Grp()
    group.groupID=groupID
    group.group_name=group_name
    current_user=request.user
    username=current_user.username
    groupAssociation=GroupAssociation()
    groupAssociation.username=username
    groupAssociation.groupID=groupID
    groupAssociation.group_name=group_name
    groupAssociation.isAdmin='true'
    if(group.group_name!=None and group.group_name!=''):
        groupAssociation.save()
        group.save()
        my_dict={'insert_me':'Group creation successful.'}

        #Begin Code
        gid=request.POST.get('gid')

        comment_list=Comment.objects.order_by('groupID')

        if(gid!=None and gid!=''):
            groupID_filter=gid
            association_list=GroupAssociation.objects.order_by('groupID')
            groupIDs=[]
            #print(association_list)
            #Check the group IDs associated with the particular member.
            for associations in association_list:
                if(request.user.username==associations.username):
                    groupIDs.append(associations.groupID)

            #Find the list of posts having the appended group IDs.
            appended_posts=Post.objects.order_by('groupID')
            post_list=[]
            for p in appended_posts:
                if p.groupID==groupID_filter:
                    post_list.append(p)

            #Check if the user has contributed a comment or not.
            user_contribution=0
            for c in comment_list:
                if(c.username==request.user.username and c.groupID==groupID_filter):
                    user_contribution=1
            #End check if user has contributed a comment or not.

            #Check if the user has contributed a comment or not.
            user_contribution=0
            for c in comment_list:
                if(c.username==request.user.username and c.groupID==groupID_filter):
                    user_contribution=1
            #End check if user has contributed a comment or not.

            #print(post_list)
            association_dict={'association':post_list,'group_no':groupID_filter,'clist':comment_list,'contributed':user_contribution}
            return render(request,'basic_app/view_posts.html',context=association_dict)
        association_list=GroupAssociation.objects.order_by('groupID')
        association_dict={'association':association_list}
        return render(request,'basic_app/load_quiz.html',context=association_dict)
        #End Code

        #return render(request,'basic_app/load_quiz.html',context=my_dict)
    #my_dict={'insert_me':'Booking failed.'}
    return render(request,'basic_app/quiz.html')

def load_quiz(request):
    gid=request.POST.get('gid')

    comment_list=Comment.objects.order_by('groupID')

    if(gid!=None and gid!=''):
        #Check if the user has contributed a comment or not.
        user_contribution=0

        for c in comment_list:
            if(c.username    ==request.user.username and c.groupID==gid):
                user_contribution=1
        #End check if user has contributed a comment or not.

        groupID_filter=gid
        association_list=GroupAssociation.objects.order_by('groupID')
        groupIDs=[]
        #print(association_list)
        #Check the group IDs associated with the particular member.
        for associations in association_list:
            if(request.user.username==associations.username):
                groupIDs.append(associations.groupID)

        #Find the list of posts having the appended group IDs.
        appended_posts=Post.objects.order_by('groupID')
        post_list=[]
        for p in appended_posts:
            if p.groupID==groupID_filter:
                post_list.append(p)

        #print(post_list)
        association_dict={'association':post_list,'group_no':groupID_filter,'clist':comment_list,'contributed':user_contribution}
        return render(request,'basic_app/view_posts.html',context=association_dict)
    association_list=GroupAssociation.objects.order_by('groupID')
    association_dict={'association':association_list}
    return render(request,'basic_app/load_quiz.html',context=association_dict)

def add_member(request):
    groupID=request.POST.get('gid')
    membername=None

    #Find the list of users who have been checkboxed.
    all_user=User.objects.order_by('username')
    selected_users_to_add=[]
    for user in all_user:
        if(request.POST.get(user.username)!=None):
            selected_users_to_add.append(user.username)
            membername='somemember'

    #print(groupID)
    group_name=''

    groups=Grp.objects.order_by('groupID')
    for group in groups:
        if group.groupID==groupID:
            group_name=group.group_name

    if(groupID!=None and membername!=None):
        user_list=User.objects.order_by('username')

        #We check if the user is attempting to add himself or herself in the group or not.
        # member_exists=False
        # for user in user_list:
        #     if(membername==user.username and membername!=request.user):
        #         member_exists=True
        # if(member_exists==False):
        #     return HttpResponse("Invalid username of member. <a href=\"index.html\">Go home</a> ")
        association_list=GroupAssociation.objects.order_by('groupID')

        for associations in association_list:
            if(associations.username==request.user.username and groupID==associations.groupID):

                #Add all the members who have been checkboxed.
                for member in selected_users_to_add:
                    new_association=GroupAssociation()
                    new_association.username=member
                    new_association.groupID=groupID
                    new_association.group_name=group_name
                    new_association.save()

                #Begin code
                association_list=GroupAssociation.objects.order_by('groupID')
                association_dict={'association':association_list}
                return render(request,'basic_app/load_quiz.html',context=association_dict)
                #End code
        return HttpResponse("Invalid group ID. <a href=\"index.html\">Go home</a> ")
    association_list=GroupAssociation.objects.order_by('groupID')
    user_list=User.objects.order_by('username')

    #Iterate through the user list and see which user is not a member of the group.
    users_not_added=[]
    print(user_list)
    for user in user_list:
        in_group=False
        for association in association_list:
            if(association.groupID==groupID and user.username==association.username):
                in_group=True
                break
        if(in_group==False):
            users_not_added.append(user)

    association_dict={'association':association_list,'group_no':groupID,'users':users_not_added}
    return render(request,'basic_app/add_member.html',context=association_dict)

def view_members_in_groups(request):
    association_list=GroupAssociation.objects.order_by('groupID')
    groupIDs=[]

    #Check the group IDs associated with the particular member.
    for associations in association_list:
        if(request.user.username==associations.username):
            groupIDs.append(associations.groupID)

    #Find the list of members in the appended group IDs.
    member_list=[]
    for associations in association_list:
        if associations.groupID in groupIDs:
            member_list.append(associations)

    association_dict={'association':member_list}
    return render(request,'basic_app/view_members_in_groups.html',context=association_dict)

def add_post(request):
    groupID=groupID_filter
    print(groupID)
    username=request.user.username
    post_content=request.POST.get('post_content')

    group_name=''

    groups=Grp.objects.order_by('groupID')
    for group in groups:
        if group.groupID==groupID:
            group_name=group.group_name

    if(groupID!=None and username!=None):
        user_list=User.objects.order_by('username')
        association_list=GroupAssociation.objects.order_by('groupID')
        for associations in association_list:
            if(associations.username==username and groupID==associations.groupID):
                post=Post()
                post.username=username
                post.groupID=groupID
                post.group_name=group_name
                post.post_content=post_content
                post.save()
                return HttpResponse("Post successfully added. <a href=\"index.html\">Go home</a> ")
        return HttpResponse("Cannot add post. <a href=\"index.html\">Go home</a> ")

    association_list=GroupAssociation.objects.order_by('groupID')
    association_dict={'association':association_list}
    return HttpResponse("Cannot add post. <a href=\"index.html\">Go home</a> ")

def view_posts(request):
    post_content=request.POST.get('post_content')
    groupID=request.POST.get('gid')
    if(post_content==None or post_content==''):
        #print(groupID_filter)
        association_list=GroupAssociation.objects.order_by('groupID')
        #print(comment_list)
        groupIDs=[]
        #print(association_list)
        #Check the group IDs associated with the particular member.
        for associations in association_list:
            if(request.user.username==associations.username):
                groupIDs.append(associations.groupID)

        #Find the list of posts having the appended group IDs.
        appended_posts=Post.objects.order_by('groupID')
        post_list=[]
        for p in appended_posts:
            if p.groupID==groupID_filter:
                post_list.append(p)

        #Check if the user has contributed a comment or not.
        user_contribution=0

        comment_list=Comment.objects.order_by('groupID')

        for c in comment_list:
            if(c.username==request.user.username and groupID==c.groupID):
                user_contribution=1
        #End check if user has contributed a comment or not.

        #print(groupID_filter)
        if(len(post_list)==0):
            my_dict={'group_no':groupID_filter,'contributed':user_contribution}
            return render(request,'basic_app/view_posts.html',context=my_dict)

        association_dict={'association':post_list,'group_no':groupID_filter,'contributed':user_contribution}
        return render(request,'basic_app/view_posts.html',context=association_dict)
    else:
        groupID=request.POST.get('gid')
        username=request.user.username
        post_content=request.POST.get('post_content')

        group_name=''

        groups=Grp.objects.order_by('groupID')
        for group in groups:
            if group.groupID==groupID:
                group_name=group.group_name

        if(groupID!=None and username!=None):
            user_list=User.objects.order_by('username')
            association_list=GroupAssociation.objects.order_by('groupID')
            for associations in association_list:
                if(associations.username==username and groupID==associations.groupID):
                    post=Post()
                    post.username=username
                    post.groupID=groupID
                    post.group_name=group_name
                    post.post_content=post_content
                    post.save()

                    #Code begin

                    association_list=GroupAssociation.objects.order_by('groupID')
                    #print(comment_list)
                    groupIDs=[]
                    #print(association_list)
                    #Check the group IDs associated with the particular member.

                    comment_list=Comment.objects.order_by('groupID')

                    for associations in association_list:
                        if(request.user.username==associations.username):
                            groupIDs.append(associations.groupID)

                    #Find the list of posts having the appended group IDs.
                    appended_posts=Post.objects.order_by('groupID')
                    post_list=[]
                    for p in appended_posts:
                        if p.groupID==groupID:
                            post_list.append(p)

                    #print(groupID_filter)
                    if(len(post_list)==0):
                        my_dict={'group_no':groupID}
                        return render(request,'basic_app/view_posts.html',context=my_dict)

                    #Check if the user has contributed a comment or not.
                    user_contribution=0
                    for c in comment_list:
                        if(c.username==request.user.username and c.groupID==groupID):
                            user_contribution=1
                    #End check if user has contributed a comment or not.

                    comment_list=Comment.objects.order_by('groupID')
                    association_dict={'association':post_list,'group_no':groupID,'clist':comment_list,'contributed':user_contribution}
                    return render(request,'basic_app/view_posts.html',context=association_dict)
                    #Code end

                    #return HttpResponse("Post added. <a href=\"{% url 'basic_app:load_quiz'%}\">Go home</a> ")
            return HttpResponse("Cannot add post. <a href=\"index.html\">Go home</a> ")

        association_list=GroupAssociation.objects.order_by('groupID')
        association_dict={'association':association_list,'group_no':groupID}
        return HttpResponse("Cannot add post. <a href=\"index.html\">Go home</a> ")

def add_comment(request):
    #comment_list=Comment.objects.order_by('groupID')
    groupID=request.POST.get('gd')
    username=request.POST.get('uname')
    group_name=request.POST.get('gname')
    post_content=request.POST.get('pcontent')
    comment=request.POST.get('comment')
    cmt=Comment()
    cmt.groupID=groupID
    cmt.username=request.user.username
    cmt.group_name=group_name
    cmt.post_content=post_content
    cmt.comment=comment
    #print(cmt.post_content)
    cmt.save()

    #Code begin

    association_list=GroupAssociation.objects.order_by('groupID')
    #print(comment_list)
    groupIDs=[]
    #print(association_list)
    #Check the group IDs associated with the particular member.
    for associations in association_list:
        if(request.user.username==associations.username):
            groupIDs.append(associations.groupID)

    #Find the list of posts having the appended group IDs.
    appended_posts=Post.objects.order_by('groupID')
    post_list=[]
    for p in appended_posts:
        if p.groupID==groupID:
            post_list.append(p)

    #Check if the user has contributed a comment or not.
    user_contribution=0

    comment_list=Comment.objects.order_by('groupID')

    for c in comment_list:
        if(c.username==request.user.username and c.groupID==groupID):
            user_contribution=1
    #End check if user has contributed a comment or not.

    #print(groupID_filter)
    if(len(post_list)==0):
        my_dict={'group_no':groupID,'contributed':user_contribution}
        return render(request,'basic_app/view_posts.html',context=my_dict)

    #Check if the user has contributed a comment or not.
    user_contribution=0
    for c in comment_list:
        if(c.username==request.user.username):
            user_contribution=1
    #End check if user has contributed a comment or not.

    comment_list=Comment.objects.order_by('groupID')
    association_dict={'association':post_list,'group_no':groupID,'clist':comment_list,'contributed':user_contribution}
    #print(groupID)
    return render(request,'basic_app/view_posts.html',context=association_dict)

    #Code end

def delete_user_from_group(request):
    #Get the group id provided as a hidden input.
    groupID=request.POST.get('gid')

    #Get the list of users.
    list_of_users=User.objects.order_by('username')

    #Delete the user if it exists in the group and if it has been checkboxed.
    for user in list_of_users:
        curr_username=request.POST.get(user.username)
        if(curr_username!=None and curr_username!=''):
            GroupAssociation.objects.filter(username=user.username,groupID=groupID).delete()

    #Return the group details once the members have been deleted.
    association_list=GroupAssociation.objects.order_by('groupID')
    print("GroupID: ", groupID)
    association_dict={'association':association_list}
    return render(request,'basic_app/load_quiz.html',context=association_dict)

def delete_group(request):
    #Get the group id provided as a hidden input.
    groupID=request.POST.get('gid')
    print("groupID: ", groupID, " has been deleted")
    # Get the list of users.
    list_of_users = User.objects.order_by('username')

    # Delete the user if it exists in the group and if it has been checkboxed.
    for user in list_of_users:
        GroupAssociation.objects.filter(username=user.username, groupID=groupID).delete()

    Post.objects.filter(groupID=groupID).delete()

    Grp.objects.filter(groupID=groupID).delete()
    print("group: ", groupID, " has been deleted")

    #Return the group details once the members have been deleted.
    association_list=GroupAssociation.objects.order_by('groupID')
    association_dict={'association':association_list}
    return render(request,'basic_app/load_quiz.html',context=association_dict)

