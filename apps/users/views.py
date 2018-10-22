from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
import bcrypt
from .models import *

def index(request):
    if 'id' in request.session:
        return redirect('/home')

    return render(request, 'users/index.html')

def register(request):
    errors = User.objects.validator(request.POST)

    if len(errors):
        for tag, error in errors.items():
            messages.error(request, error)
        return redirect('/')
    else:
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        
        User.objects.create(first_name=first_name, last_name=last_name, email=email, password=pw_hash)
        user = User.objects.get(email=email)
        request.session['id'] = user.id

        messages.success(request, "Successfully Registered!")
        return redirect('/home')

def home(request):
    if 'id' not in request.session:
        return redirect('/')

    user = User.objects.get(id=request.session['id'])
    return render(request, 'users/home.html', {'user': user})

def login(request):
    email = request.POST['email']
    password = request.POST['password']

    user = User.objects.filter(email=email)
    if len(user) > 0:
        if bcrypt.checkpw(password.encode(), user[0].password.encode()):
            request.session['id'] = user[0].id
            messages.success(request, "Successfully logged in.")
            return redirect('/home')
        else:
            messages.error(request, "Incorrect email/password combination.")
            return redirect('/')

    else:
        messages.error(request, "Account does not exist.")
        return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/')
