from datetime import date, timedelta
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, logout, login as auth_login
from . models import *
from django.contrib import messages
from django.utils.crypto import get_random_string
from django.core.exceptions import ObjectDoesNotExist
from Admin.views import admindash
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password

# Create your views here.
def landing_page(request):
    return render(request,'landing_page.html')

#Login Section ------------
def login_page(request):
    return render(request,'login.html')

# def login_submitt(request):
#   if request.method == 'POST':
#     username = request.POST['username']
#     password = request.POST['password']
#     user = authenticate(username=username, password=password)

#     if user is not None and user.is_staff:
#       auth_login(request, user)
#       return redirect('admindash')

#     hashed_password = make_password(password)
#     print(hashed_password)
#     if StudentDetails.objects.filter(email = username).exists():
#         try:
#           log_user = StudentDetails.objects.get(email=username, password=hashed_password)

#           request.session["login_id"] = log_user.id
#           if 'login_id' in request.session:
#                student_id = request.session['login_id']
#                return redirect('student_dash')

#         except ObjectDoesNotExist:
#           messages.error(request, 'Invalid Username or Password. Try Again!')
#           return redirect('login_page')
        
#     if StudentDetails.objects.filter(phone = username).exists():
#         try:
#           log_user = StudentDetails.objects.get(phone=username, password=password)

#           request.session["login_id"] = log_user.id
#           if 'login_id' in request.session:
#                student_id = request.session['login_id']
#                return redirect('student_dash')
          
#         except ObjectDoesNotExist:
#           messages.error(request, 'Invalid Username or Password. Try Again!')
#           return redirect('login_page')
#     else:
#        messages.error(request, 'Invalid Username or Password. Try Again!')
#        return redirect('login_page')
        
#   return redirect('login_page')

def login_submitt(request):
  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)

    if user is not None and user.is_staff:
      auth_login(request, user)
      return redirect('admindash')

    if StudentDetails.objects.filter(email = username).exists():
        try:
          log_user = StudentDetails.objects.get(email=username)

          if check_password(password, log_user.password):
              # Password matches, set session and redirect
              request.session["login_id"] = log_user.id
              return redirect('student_dash')
          else:
              messages.error(request, 'Password is not matching. Try Again!')
              return redirect('login_page')
          
        except ObjectDoesNotExist:
            # User not found or password does not match
            messages.error(request, 'Invalid Username or Password. Try Again!')
            return redirect('login_page')
        
    if StudentDetails.objects.filter(phone = username).exists():
        try:
          log_user = StudentDetails.objects.get(phone=username)

          if check_password(password, log_user.password):
              # Password matches, set session and redirect
              request.session["login_id"] = log_user.id
              return redirect('student_dash')
          else:
              messages.error(request, 'Password is not matching. Try Again!')
              return redirect('login_page')
          
        except ObjectDoesNotExist:
            # User not found or password does not match
            messages.error(request, 'Invalid Username or Password. Try Again!')
            return redirect('login_page')
    else:
       messages.error(request, 'Invalid Username or Password. Try Again!')
       return redirect('login_page')
        
  return redirect('login_page')
        
    
       



def register_page(request):
    return render(request,'register.html')

def register_submit(request):
    if request.method == 'POST':
        name = request.POST['name']
        address = request.POST['address']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']
        pic = request.FILES.get('image')

        if not StudentDetails.objects.filter(email = email).exists():
            if not StudentDetails.objects.filter(phone = phone).exists():
                
                hashed_password = make_password(password)
                
                student_data =StudentDetails(
                name = name,
                address = address,
                email = email,
                phone = phone,
                username = phone,
                password = hashed_password,
                image=pic,
                )
                student_data.save()
                return redirect('login_page')

            else:
                messages.info(request, 'Sorry, Phone number already exists!')
                return redirect('register_page')
            
        else:
            messages.info(request, 'Sorry, Email already exists!')
            return redirect('register_page')
        
    return redirect('register_page')


def check_email(request):

    if request.method == 'GET':
        email = request.GET.get('email', '')

        exists = StudentDetails.objects.filter( email=email).exists()

        return JsonResponse({'exists': exists})

    return JsonResponse({'exists': False})  
        

def check_phone(request):

    if request.method == 'GET':
        ph = request.GET.get('ph', '')

        exists = StudentDetails.objects.filter( phone=ph).exists()

        return JsonResponse({'exists': exists})

    return JsonResponse({'exists': False})  
        
      







#Logout section----------------------
    
def admin_logout(request):
  auth.logout(request)
  return redirect('landing_page')

def student_logout(request):
  request.session.pop('login_id', None)
  return redirect('landing_page')   