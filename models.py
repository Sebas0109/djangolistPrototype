from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password

# Create your models here.

class UserManager(BaseUserManager):

    def create_user(self, username, first_name, last_name, email, password = None):

        if username is None:
            raise TypeError('Users should have a username')
        if email is None:
            raise TypeError('Users should have a email')
        if first_name is None:
            raise TypeError('Users should have a First Name')
        if last_name is None:
            raise TypeError('Users should have a Last Name')

        user=self.model(username = username, first_name=first_name, last_name=last_name,
                         email=self.normalize_email(email))
        #Pass = make_password(password)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, first_name, last_name, email, password=None):
        if password is None:
            raise TypeError('Password should not be None')

        user = self.create_user(username, first_name, last_name, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.is_clinic_admin = True
        user.save()
        return user

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length = 30, unique = True, db_index = True)
    first_name = models.CharField(max_length= 50)
    last_name = models.CharField(max_length= 75)
    email = models.EmailField(max_length=255, unique = True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_clinic_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(default=False)
    
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return self.email

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            #In this method we will return the two tokens of the user
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }


"""
class UserManager(BaseUserManager):
    #Overriding Creation of a user 
    def create_user(self, username, first_name, last_name, email, password = None):

        if username is None:
            raise TypeError('Users should have a username')
        if email is None:
            raise TypeError('Users should have a email')
        if first_name is None:
            raise TypeError('Users should have a First Name')
        if last_name is None:
            raise TypeError('Users should have a Last Name')


        user=User(username = username, first_name=first_name, last_name=last_name,
                         email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, first_name, last_name, email, password=None):
        if password is None:
            raise TypeError('Password should not be None')

        user = self.create_user(username, first_name, last_name, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.is_clinic_admin = True
        user.save(using=self._db)
        return user
"""