from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse,HttpResponseRedirect
from app.forms import *
from app.models import *
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required

def registration(request):
    UFO = UserForm()
    PFO = ProfileForm()
    d = {'UFO':UFO,'PFO':PFO}
    
    if request.method == 'POST' and request.FILES :
        ufd = UserForm(request.POST)
        pfd = ProfileForm(request.POST,request.FILES)

        if ufd.is_valid() and pfd.is_valid():
            MUFDO = ufd.save(commit=False)
            MUFDO.set_password(ufd.cleaned_data['password'])
            MUFDO.save()

            MPFDO = pfd.save(commit=False)
            MPFDO.username = MUFDO
            MPFDO.save()

            
            send_mail(
                'Registration',
                'Registration is Successful',
                'sreenugattu5@gmail.com',
                [MUFDO.email],
                fail_silently=False
            )

            return HttpResponse('Successful')
        else:
            return HttpResponse('Invalid Data')
        
    return render(request,'registration.html',d)

def user_login(request):
    if request.method == 'POST':
        username = request.POST['un']
        password = request.POST['pw']
        AUO = authenticate(username = username,password = password)
        if AUO and AUO.is_active :
            login(request,AUO)
            request.session['username'] = username
            return HttpResponseRedirect(reverse('home')) # hold the login req,session and auo. Now redirect to Home function
        else:
            return HttpResponse('Invalid Credentials')

    return render(request,'user_login.html')

def home(request):
    if request.session.get('username'): 
        username = request.session.get('username')
        d = {'username':username}
        return render(request,'home.html',d)
    return render(request,'home.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

@login_required
def display_profile(request):
    un = request.session.get('username')
    uo = User.objects.get(username = un)
    po = Profile.objects.get(username = uo)
    d = {'uo':uo,'po':po}
    return render(request,'display_profile.html',d)

@login_required
def change_password(request):
    if request.method == 'POST':
        password = request.POST['pw']
        rpassword = request.POST['rpw']
        if password != rpassword:
            return HttpResponse('Passwords not matching')
        username = request.session.get('username')
        uo = User.objects.get(username = username)
        uo.set_password(password)
        uo.save()
        return HttpResponseRedirect(reverse('user_login'))
    return render(request,'change_password.html')

def forget_password(request):
    if request.method == 'POST':
        username = request.POST['un']
        LUO = User.objects.filter(username = username)
        if LUO:
            uo = LUO[0]
            password = request.POST['pw']
            rpassword = request.POST['rpw']
            if password != rpassword:
                return HttpResponse('Passwords not matching')
            uo.set_password(password)
            uo.save()
            return HttpResponseRedirect(reverse('user_login'))
        return HttpResponse('User Data is Not available in Database')

    return render(request,'forget_password.html')