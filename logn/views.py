from django.shortcuts import render ,redirect
from django.contrib.auth.models import  auth
from logn.models import CustomUser,Students
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from finalpro import settings
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from logn.models import Contact

# Create your views here.
def home(request):
    return render(request,'logn/home.html')


def about(request):
    return render(request,'logn/about2.html')
def contact_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        name=request.POST.get("name") 
        email=request.POST.get("email") 
        comment=request.POST.get("comment") 
        try:
            contact_model=Contact(name=name,email=email,comment=comment)
            contact_model.save()
            messages.success(request,"Successfully Added Notification")
            return HttpResponseRedirect("logn/contact")
        except:
            messages.error(request,"Failed To Add Notification")
            return HttpResponseRedirect("logn/contact")    

def contact(request):

    return render(request,'logn/contact.html')   

def homeadmin_template(request):
    
    return render(request,'logn/homeadmin_template.html')

def register(request):
     if request.method=='POST':
        username=request.POST.get("username")
        email=request.POST.get('email')
        password1=request.POST.get('password1')
        password2=request.POST.get('password2') 
        
       
        if password1==password2:
            if CustomUser.objects.filter(username=username).exists():
                messages.info(request,'USERNAME TAKEN') 
                return redirect('register')
            elif CustomUser.objects.filter(email=email).exists():  
                messages.info(request,'EMAIL TAKEN')
                return HttpResponseRedirect(reverse('register'))

            else:
                user=CustomUser.objects.create_user(username=username,email=email,password=password1,user_type=3)
                user.save();
                print('user created')
                return redirect('login')
        else:
            print('password mot matching')
            return redirect('/')

     return render(request,'logn/register.html')   








"""def login(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        user=EmailBackEnd.authenticate(request,username=request.POST.get("email"),password=request.POST.get("password"))
        if user!=None:
            login(request,user)
            if user.user_type=="1":
                return HttpResponseRedirect('/admin_home')
            elif user.user_type=="2":
                return HttpResponseRedirect(reverse("staff_home"))
            elif:
                return HttpResponseRedirect(reverse("student_home"))
            elif
                messages.error(request,"Invalid Login Details")
                return HttpResponseRedirect("/")
        else:
            return render(request,'logn/login.html')"""


"""
def login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']

        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            if user.user_type =="1":
                 return redirect('homeadmin_template')
            elif user.user_type =="2":
                 return redirect('faculty_home')
            elif user.user_type =="3":
                 return redirect('student_home')
        else:
             messages.error(request,"Invalid Login Details")
             return redirect('login')    
    else:
        return render(request,'logn/login.html')"""


def loginn(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(username=username,password=password)
        print(user)

        if user is not None:
            login(request,user)
            print(user.id)
            try:
                request.session['user'] = user.student.id
            except:
                request.session['user'] = user.id
            if user.user_type =="1":
                 return HttpResponseRedirect(reverse("homeadmin_template"))
            elif user.user_type =="2":
                 return HttpResponseRedirect(reverse("faculty_home"))
            elif user.user_type =="3":
                 return  HttpResponseRedirect(reverse("student_home"))
        else:
             messages.error(request,"Invalid Login Details")
             return HttpResponseRedirect(reverse("login"))
    else:
        return render(request,'logn/login.html')




def loogout(request):
    logout(request)
    return HttpResponseRedirect("/")

     




 