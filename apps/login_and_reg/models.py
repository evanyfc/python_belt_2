from __future__ import unicode_literals
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
import datetime
import bcrypt
#import re
#email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.

class UserManager(models.Manager):
    def validateLogin(self, form_data):
        errors = []
        try:
            user = User.objects.get(username=form_data['username'])
            password = form_data['password'].encode()
            if bcrypt.hashpw(password, user.pw_hash.encode()) == user.pw_hash.encode():
                return (True, user)
            else:
                errors.append("Incorrect password!")
        except ObjectDoesNotExist:
            errors.append("Username does not exist")
            return (False, errors)

    def register(self, form_data):
        errors = []
        name = form_data['name']
        username = form_data['username']
        if not name or name.isspace():
            erros.append("Please enter a name")
        elif len(name) < 3:
            errors.append("Your name must be longer than three characters")
        if not username or username.isspace():
            errors.append("Please enter a username")
        elif len(username) < 3:
            errors.append("Your username must be longer than three characters")
        elif self.filter(username=username).exists():
            errors.append(("Username already exists!"))
        if not form_data['date_hired']:
            errors.append("Please enter your hiring date")
        if len(form_data['password']) < 8:
            errors.append("Password must be at least 8 characters")
        elif not form_data['password'] == form_data['confirm_password']:
            errors.append("Passwords do not match")

        if len(errors):
            return (False, errors)

        pw_hash = bcrypt.hashpw(form_data['password'].encode(), bcrypt.gensalt())
        user = self.create(name = form_data['name'], username = form_data['username'], pw_hash = pw_hash, date_hired = form_data['date_hired'])
        return (True, user)

class User(models.Model):
    name = models.CharField(max_length=45)
    username = models.CharField(max_length=45)
    pw_hash = models.CharField(max_length=255)
    date_hired = models.DateField(default=datetime.date.today)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = UserManager()
