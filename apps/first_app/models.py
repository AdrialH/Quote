from __future__ import unicode_literals
from django.db import models
import bcrypt
import re 

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+-]+@[a-zA-Z0-9.-]+.[a-zA-Z]+$')

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        
        if len(postData['firstname']) < 2:
            errors["first_name"] = "First name should be at least 2 characters."
        elif not str.isalpha(postData['firstname']):
            errors["first_name"] = "First name can not contain numbers."
        elif not str.istitle(postData['firstname']):
            errors["first_name"] = "First letter of First Name must be capatalized."
        
        if len(postData['lastname']) < 2:
            errors["last_name"] = "Last name should be at least 2 characters."
        elif not str.isalpha(postData['lastname']):
            errors["last_name"] = "Last name can not contain numbers."
        elif not str.istitle(postData['lastname']):
            errors["last_name"] = "First letter of Last Name must be capatalized."
        
        if len(postData['email']) < 1:
            errors["email"] = "Email is required."
        if len(postData['email']) > 40:
            errors["email"] = "Email is required to be coreect format,also no longer than forthy characters."
        elif not EMAIL_REGEX.match(postData['email']): 
            errors["email"] = "Must be valid email."
        
        if len(postData['password']) < 8:
            errors['password'] = "Password must be more than 8 characters long."
        elif not str.isalnum(postData['password']):
            errors['password'] = "Password must contain one or more numbers."
        elif len(postData['password']) > 10:
                errors["password"] = "Password can not be more than ten characters."
        elif str.isupper(postData['password']):
            errors['password'] = "Password can not be all caps."
        if not len(postData['passwordconfirmation']) == len(postData['password']):
            errors['passwordconfirmation'] = "Passwords do not match."
        
        
        return errors
    
    def login_validator(self, postData):
        errors = {}
        
        
        if len(postData['email']) < 1:
            errors["email"] = "Email can not be empty."
        elif not EMAIL_REGEX.match(postData['email']): 
            errors["email"] = "Must be valid email."
        elif not User.objects.filter(email = postData['email']).exists():
            errors["email"] = "This email does not exist, please register first."
        
        elif len(postData['password']) < 1:
            errors["password"] = "Password can not be empty."
        elif len(postData['password']) > 10:
            errors["password"] = "Password can not be more than ten characters."
        if User.objects.filter(email = postData['email']).exists():
            user = User.objects.get(email = postData['email'])
            if not bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
                errors['password'] = "Password does not match the one used to create account."
       
        return errors

    def update_validator(self, postData):
        errors = {}
        if len(postData['firstname']) < 1:
            errors["first_name"] = "First name must be updated with all other informatin."
        elif not str.isalpha(postData['firstname']):
            errors["first_name"] = "First name can not contain numbers."
        elif not str.istitle(postData['firstname']):
            errors["first_name"] = "First letter of First Name must be capatalized."
        
        if len(postData['lastname']) < 1:
            errors["last_name"] = "Last name must be updated with all other informatin."
        elif not str.isalpha(postData['lastname']):
            errors["last_name"] = "Last name can not contain numbers."
        elif not str.istitle(postData['lastname']):
            errors["last_name"] = "First letter of Last Name must be capatalized."
        
        if len(postData['email']) < 1:
            errors["email"] = "Email must be updated with all other informatin."
        elif not EMAIL_REGEX.match(postData['email']): 
            errors["email"] = "Must be valid email."
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = UserManager()
    

    def __repr__(self):
        return "<User {}|{}{}{}{}>".format(self.id,self.first_name,self.last_name, self.email)

class MessageManager(models.Manager):
    def message_validator(self, postData):
        errors = {}
        if Message.objects.filter(item = postData['post']).exists():
            errors['message'] = "Quote already exist on someone else's list."
        if len(postData['post']) > 50: 
            errors['message'] = "Quote is to long, must be less than 50 charaters."
        elif len(postData['post']) < 1:
            errors['message'] = "Quote must contain content."
        return errors
        



class Message(models.Model):
    item = models.CharField(max_length=255)
    user_post = models.ForeignKey('User', on_delete=models.CASCADE, related_name = "post")
    mes_liked = models.ManyToManyField('User', related_name= "likes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = MessageManager()

    

    def __repr__(self):
        return "<User {}|{}{}>".format(self.id,self.item,self.user_post)



        