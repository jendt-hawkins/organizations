from django.db import models
import re
from datetime import datetime

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def basic_validator(self, postData):

        errors = {}

        if len(postData['first_name'])<2:
            errors['first_name'] = "First name must be at least 2 characters"

        if len(postData['last_name'])<2:
            errors['last_name'] = "Last name must be at least 2 characters"

        if len(postData['email'])<1:
            errors['email'] = "Email cannot be blank"
        elif not EMAIL_REGEX.match(postData['email']):               
            errors['email'] = "Invalid email address"

        if len(postData['password'])<8:
            errors['password'] = "Password must be at least 8 characters"

        if postData['password'] != postData['confirm']:
            errors['passwords'] = "Passwords must match"

        user = User.objects.filter(email=postData['email'])
        if len(user) != 0:
            errors['login_email']="This email has already been registered"

        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = UserManager()


class OrganizationManager(models.Manager):

    def organization_validator(self, postData):

        errors = {}

        if len(postData['name'])<5:
            errors['name'] = "Organization name must be at least 5 characters" 

        if len(postData['description'])<10:
            errors['description'] = "Description must be at least 10 characters"

        return errors

class Organization(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    uploaded_by = models.ForeignKey(User, related_name="organization_uploaded", on_delete = models.CASCADE)
    joined_by = models.ManyToManyField(User, related_name="joined_organizations")

    objects = OrganizationManager()
