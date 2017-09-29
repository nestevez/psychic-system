# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib import messages
from ..travels import urls
from .models import *
from .forms import *

#renders and validates login and registration forms
def logreg(request):
    if request.method == 'POST':
        data = request.POST
        errors=[]
        if 'cpw' in data:
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
    'log_form': LogForm,
    }
    return render(request, 'users/logreg.html', context)

#submits a valid registration data, sets the session and redirects to dashboard
def register(request):
    data = request.POST
    pwhash = bcrypt.hashpw(data['pw'].encode(), bcrypt.gensalt(10))
    Users.objects.create(name=data['name'], uname=data['uname'], pw=pwhash)
    set_session(request)
    return redirect('travels:dashboard')

#sets the session when login is valid and redirects to dashboard
def login(request):
    set_session(request)
    return redirect('travels:dashboard')

#sets the session: sets email as user identifier, sets access as appropriate and sets logged to true
def set_session(request):
    request.session['user']=request.POST['uname']
    request.session['logged']=True

#clears the session and logs user out
def logout(request):
    request.session.clear()
    request.session['logged']=False
    return redirect('users:logreg')
