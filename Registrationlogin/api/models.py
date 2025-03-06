from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self, username, first_name, last_name, email, password=None, password2=None):
        if not username:
            raise ValueError("Users must have a username")
        if not password:
            raise ValueError("Users must have a password")

        email = self.normalize_email(email)
        user = self.model(username=username, first_name=first_name, last_name=last_name, email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):  
    username = models.CharField(max_length=50, unique=True)  
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    def __str__(self):
        return self.username

  