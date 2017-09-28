# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from .models import *
from .forms import *

#renders and validates login and registration forms
def logreg(request):
    if request.method == 'POST':
        data = request.POST
        errors=[]
        if 'fname' in data:
            errors = Users.objects.reg_valid(data)
            if len(errors):
                for tag, error in errors.iteritems():
                    messages.error(request, error, extra_tags=tag)
            else:
                return register(request)
        else:
            errors = Users.objects.login_valid(data)
            if len(errors):
                for tag, error in errors.iteritems():
                    messages.error(request, error, extra_tags=tag)
            else:
                return login(request)
    context = {
    'title': "Login and Registration",
    'reg_form': RegForm,
    'pass_form': PassForm,
    'log_form': LogForm,
    }
    return render(request, 'users/logreg.html', context)

#submits a valid registration data and sets the session
def register(request):
    data = request.POST
    pwhash = bcrypt.hashpw(data['pw'].encode(), bcrypt.gensalt(10))
    Users.objects.create(fname=data['fname'], lname=data['lname'], email=data['email'], pw=pwhash)
    set_session(request)
    return success(request)

#sets the session when login is valid
def login(request):
    set_session(request)
    return success(request)

#sets the session: sets email as user identifier, sets access as appropriate and sets logged to true
def set_session(request):
    request.session['user']=request.POST['email']
    request.session['access']=Users.objects.get(email=request.POST['email']).access_level
    request.session['logged']=True

#checks if user is logged in. if not, redirects to login page
def log_check(request):
    if request.session['logged']==False:
        return redirect('/')

#renders a success page for successful login
def success(request):
    context = {
    'title': "Successful Initiation"
    }
    return render(request,'users/success.html', context)

#clears the session and logs user out
def logout(request):
    request.session.clear()
    request.session['logged']=False
    return redirect('/')
