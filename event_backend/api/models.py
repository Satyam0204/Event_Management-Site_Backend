from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
# Create your models here.

class UserManager(BaseUserManager):
    use_in_migrations=True

    def create_user(self, email, password=None,**extra_fields):
        if not email:
            raise ValueError('Email is required')

        email=self.normalize_email(email)
        user=self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        extra_fields.setdefault('is_active',True)

        return user

    def create_superuser(self,email,password,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)


        if extra_fields.get('is_staff') is not True:
            raise ValueError(('Super user must have staff True'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(('Super user must have superuser True'))
        
        return self.create_user(email,password,**extra_fields)

class User(AbstractUser):
    username=None
    email = models.EmailField(unique=True)



    USERNAME_FIELD='email'
    REQUIRED_FIELDS=[]
    objects = UserManager()

    def name(self):
        return self.first_name+' '+self.last_name

    def __str__(self):
        return self.email