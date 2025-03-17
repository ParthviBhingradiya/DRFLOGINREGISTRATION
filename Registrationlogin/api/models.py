from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.exceptions import ValidationError

class UserManager(BaseUserManager):
    def create_user(self, username, first_name, last_name, email, password=None, password2=None,role=None):
        if not username:
            raise ValueError("Users must have a username")
        if not password:
            raise ValueError("Users must have a password")

        email = self.normalize_email(email)
        user = self.model(username=username, first_name=first_name, last_name=last_name, email=email,role=role)
        user.set_password(password)
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):  

    role = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    ]

    username = models.CharField(max_length=50, unique=True)  
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=role)

    # Create User
    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    def __str__(self):
        return self.username


class ApplicationForm(models.Model):

    study_mode = [
        ('online','Online'),
        ('offline','Offline'),
    ]

    status = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    university_name = models.CharField(max_length=255)
    program_name = models.CharField(max_length=255)
    description = models.TextField()
    study_mode = models.CharField(max_length=20, choices=study_mode)
    from_date = models.DateField() 
    to_date = models.DateField()
    status = models.CharField(max_length=10, choices=status, default='pending') 


    def __str__(self):
        return f"{self.program_name} at {self.university_name} by {self.user.username}"
