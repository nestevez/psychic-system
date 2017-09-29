# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from ..users.models import *
import datetime

class TripsManager(models.Manager):
    def date_check(self, year, month, day):
        today = datetime.date.today()
        print month, today.month
        if year < today.year:
            return False
        elif year == today.year:
            if month < today.month:
                return False
            elif month == today.month:
                if day <= today.day:
                    return False
        return True

    def valid_daterange(self, data):
        if data['enddate_year'] < data['startdate_year']:
            return False
        elif data['enddate_year'] == data['startdate_year']:
            if data['enddate_month'] < data['startdate_month']:
                return False
            elif data['enddate_month'] == data['startdate_month']:
                if data['enddate_day'] < data['startdate_day']:
                    return False
        return True

    def dates_valid(self, data):
        errors = {}
        if Trips.objects.date_check(int(data['startdate_year']), int(data['startdate_month']), int(data['startdate_day'])) == False or Trips.objects.date_check(int(data['enddate_year']), int(data['enddate_month']), int(data['enddate_day'])) == False:
            errors['dates']="Please choose future dates."
        else:
            if Trips.objects.valid_daterange(data) == False:
                errors['future']="Please choose a 'to' date past the 'from' date."
        return errors

class Trips(models.Model):
    destination = models.CharField(max_length=255)
    description = models.TextField()
    startdate = models.DateField()
    enddate = models.DateField()
    creator = models.ForeignKey(Users, related_name='created')
    travelers = models.ManyToManyField(Users, related_name='joined', default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TripsManager()
