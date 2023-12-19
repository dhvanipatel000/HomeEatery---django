from pyexpat.errors import messages
from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from deliveryApp.models import *
from deliveryApp.models import Customer
from django.contrib import messages

# Create your views here.
def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user  = authenticate(username=username,password=password)
        if user is not None :
            login(request,user)
            return redirect('/')
        messages.error(request,"Login Failed!! Please enter correct credentials :) ")
    return render(request,'accounts/login.html')

def user_register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone_no = request.POST.get('phone_no')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        #print(username,email)
        if password==confirm_password:
            if User.objects.filter(username=username).exists():
                messages.info(request,"Username already exists !! Please try again!!")
            else :
                if User.objects.filter(email=email).exists():
                    messages.info(request,"Email already exists !! Please try again!!")
                    return redirect('user_register')
                else :
                    user = User.objects.create_user(username=username,email=email,password=password)
                    user.save()
                    data = Customer(user=user,phone_no=phone_no)
                    data.save()
                    

                    our_user = authenticate(username=username,password=password)
                    if our_user is not None :
                        login(request,user)
                        return redirect('/')
        else:
            messages.info(request,"Password and Confirm Password must be similar ")
            return redirect('/')
    return render(request,'accounts/register.html')

def user_logout(request):
    logout(request)
    return redirect('/')

def user_profile(request):
    return render(request,'accounts/user_profile.html')
