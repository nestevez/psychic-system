# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from ..users.views import *
from .models import *
from .forms import *
import time, datetime

# Create your views here.
def dashboard(request):
    if request.session['logged']==False:
        return redirect('users:logreg')
    user = Users.objects.get(uname=request.session['user'])
    names = user.name.split(' ')
    firstname = names[0]
    trips = Trips.objects.all()
    trips_going = trips.filter(travelers=user).order_by('destination').distinct()|trips.filter(creator=user).order_by('destination').distinct()
    try:
        trips_avail = trips.exclude(creator=user).exclude(travelers=user)
    except ValueError:
        trips_avail = []
    context ={
    'title': 'Travel Dashboard',
    'firstname': firstname,
    'trips_going': trips_going,
    'trips_avail':trips_avail,
    }
    return render(request, 'travels/dashboard.html', context)

def details(request, trip_id):
    if request.session['logged']==False:
        return redirect('users:logreg')
    try:
        trip = Trips.objects.get(id=trip_id)
    except Trips.DoesNotExist:
        return redirect('trips:dashboard')
    try:
        travelers = trip.travelers.all()
    except Trips.DoesNotExist:
        travelers = []
    context = {
    'title': 'Destination',
    'trip': trip,
    'travelers': travelers,
    }
    return render(request, 'travels/details.html', context)

def addtrip(request):
    if request.session['logged']==False:
        return redirect('users:logreg')
    if request.method == 'POST':
        data = request.POST
        errors = []
        errors = Trips.objects.dates_valid(data)
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
        else:
            return create_trip(request, data)
    context = {
    'title': 'Add Plan',
    'form': NewTrip,
    }
    return render(request, 'travels/addplan.html', context)

def create_trip(request, data):
    creator = Users.objects.get(uname=request.session['user'])
    startdate = datetime.datetime(year=int(data['startdate_year']), month=int(data['startdate_month']), day=int(data['startdate_day']))
    enddate = datetime.datetime(year=int(data['enddate_year']), month=int(data['enddate_month']), day=int(data['enddate_day']))
    Trips.objects.create(destination=data['destination'], description=data['description'], startdate=startdate, enddate=enddate, creator=creator)
    return redirect('travels:dashboard')

def join(request, trip_id):
    if request.session['logged']==False:
        return redirect('users:logreg')
    trip = Trips.objects.get(id=trip_id)
    user = Users.objects.get(uname=request.session['user'])
    trip.travelers.add(user)
    return redirect('travels:dashboard')
