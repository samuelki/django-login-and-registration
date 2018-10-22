from django.db import models
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

class UserManager(models.Manager):
    def validator(request, postData):
        errors = {}

        # validate first name
        if len(postData['first_name']) < 2 or not postData['first_name'].isalpha():
            if len(postData['first_name']) < 2:
                errors['first_name_length'] = "First name must be at least 2 characters."
            if not postData['first_name'].isalpha():
                errors['first_name_alpha'] = "First name can only contain letters."

        # validate last name
        if len(postData['last_name']) < 2 or not postData['last_name'].isalpha():
            if len(postData['last_name']) < 2:
                errors['last_name_length'] = "Last name must be at least 2 characters."
            if not postData['last_name'].isalpha():
                errors['last_name_alpha'] = "Last name can only contain letters."

        # validate email
        try:
            validate_email(postData['email'])
        except ValidationError:
            errors['email'] = "Invalid email address."
        else:
            if User.objects.filter(email=postData['email']):
                errors['email'] = "Email is already in use."

        # validate password
        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters long."
        
        if postData['password'] != postData['confirm_pw']:
            errors['confirm_pw'] = "Password do not match."

        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()