# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import re, bcrypt

# Create your models here.
class UsersManager(models.Manager):
    def name_valid(self, name):
        if re.match("^[A-Za-z ]*$", name):
            return True
        else:
            return False

    def email_exists(self, email):
        try:
            exists = Users.objects.get(email=email)
            return True
        except Users.DoesNotExist:
            return False

    def reg_valid(self, data):
        errors = {}
        if not Users.objects.name_valid(data['fname']) or not Users.objects.name_valid(data['lname']):
            errors['name'] = "Names can only contain letters."
        if Users.objects.email_exists(data['email']):
            errors['email'] = "Email already taken."
        if data['pw'] != data['cpw']:
            errors['pw'] = "Password and confirmation must match."
        return errors

    def login_valid(self, data):
        errors = {}
        err = False
        if Users.objects.email_exists(data['email']):
            saved = Users.objects.get(email=data['email']).pw
            if not bcrypt.checkpw(data['pw'].encode(), saved.encode()):
                err = True
        else:
            err = True
        if err == True:
            errors['login'] = "Email and password combination does not match any records."
        return errors



class Users(models.Model):
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    email = models.CharField(max_length=255)
    pw = models.CharField(max_length=255)
    access_level = models.CharField(max_length=50, default="User")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UsersManager()
