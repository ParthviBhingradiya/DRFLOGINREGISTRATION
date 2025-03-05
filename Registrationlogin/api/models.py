from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# class UserManager(BaseUserManager):
#     def create_user(self, username, first_name, last_name, email, password=None):
#         """
#         Creates and saves a User with the given email, username, and password.
#         """
#         if not username:
#             raise ValueError("Users must have a username")
#         if not email:
#             raise ValueError("Users must have an email")

#         email = self.normalize_email(email)
#         user = self.model(username=username, first_name=first_name, last_name=last_name, email=email)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

# class Student(AbstractBaseUser, PermissionsMixin):  # Added PermissionsMixin
#     username = models.CharField(max_length=50, unique=True)  # Added max_length
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)
#     email = models.EmailField(unique=True)

#     objects = UserManager()

#     USERNAME_FIELD = 'username'  # Required for custom user models
#     REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

#     def __str__(self):
#         return self.email


  
class Student(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.username
