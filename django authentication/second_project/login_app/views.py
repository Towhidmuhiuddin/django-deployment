from django.shortcuts import render
from login_app.forms import UserForm,UserInfoForm
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from login_app.models import UserInfo

# Create your views here.
def login_page(request):
    diction = {}
    return render(request,'login_app/login.html',context=diction)

def user_login(request):
    if request.method =='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse("login_app:index"))
            else:
                return HttpResponse("Account is not active!")
        else:
            return HttpResponse("Username or password is wrong!")
    return HttpResponseRedirect(reverse('login_app:login_page'))

@login_required
def logout_page(request):
    logout(request)
    return HttpResponseRedirect(reverse('login_app:login_page'))

def index(request):
    diction = {}
    if request.user.is_authenticated:
        current_user = request.user
        user_id = current_user.id 
        user_basic_form = User.objects.get(pk=user_id)
        user_more_form = UserInfo.objects.get(user__pk=user_id)
        diction = {'basic_form':user_basic_form, 'more_info_form':user_more_form}
        
    return render(request,'login_app/index.html',context=diction)

def userform(request):
    registered = False
    if request.method =='POST':
        userform = UserForm(data=request.POST)
        userinfoForm = UserInfoForm(data=request.POST)
        if userform.is_valid() and userinfoForm.is_valid():
            user = userform.save()
            user.set_password(user.password)
            user.save()

            usercustomForm = userinfoForm.save(commit=False)
            usercustomForm.user=user
            if 'profile_pic' in request.FILES:
                usercustomForm.profile_pic = request.FILES['profile_pic']
            usercustomForm.save()
            registered=True    
    else:
        userform = UserForm()
        userinfoForm = UserInfoForm()
    diction = {'userform':userform,'userinfoform':userinfoForm,'registered':registered}
    return render(request,'login_app/userform.html',context=diction)
