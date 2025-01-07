from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin, BaseUserManager

# Create your models here.
class UserManager(BaseUserManager):

    def create_user(self, first_name, last_name, email, password = None, **extra_field):
        if not email:
            raise ValueError("email is mandatory")
        email = self.normalize_email(email)
        user = self.model(first_name = first_name, last_name = last_name, email = email, **extra_field)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, first_name, last_name, email, password, **extra_field):
        extra_field.setdefault('is_staff', True)
        extra_field.setdefault('is_superuser', True)

        if extra_field.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_field.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(first_name, last_name, email, password, **extra_field)

class User(AbstractUser, PermissionsMixin):
   
    username = None
    email = models.EmailField(unique=True)
    
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name']
