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

    def uname_exists(self, uname):
        try:
            exists = Users.objects.get(uname=uname)
            return True
        except Users.DoesNotExist:
            return False

    def reg_valid(self, data):
        errors = {}
        if not Users.objects.name_valid(data['name']):
            errors['name'] = "Names can only contain letters."
        if Users.objects.uname_exists(data['uname']):
            errors['uname'] = "Username already taken."
        if data['pw'] != data['cpw']:
            errors['pw'] = "Password and confirmation must match."
        return errors

    def login_valid(self, data):
        errors = {}
        err = False
        if Users.objects.uname_exists(data['uname']):
            saved = Users.objects.get(uname=data['uname']).pw
            if not bcrypt.checkpw(data['pw'].encode(), saved.encode()):
                err = True
        else:
            err = True
        if err == True:
            errors['login'] = "Username and password combination does not match any records."
        return errors



class Users(models.Model):
    name = models.CharField(max_length=50)
    uname = models.CharField(max_length=50)
    pw = models.CharField(max_length=255)
    access_level = models.CharField(max_length=50, default="User")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UsersManager()
