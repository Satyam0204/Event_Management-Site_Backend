from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.core.validators import MinValueValidator, MaxValueValidator
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


class Event(models.Model):
    name=models.CharField(max_length=500)
    desc=models.TextField(max_length=500)
    start_date=models.DateTimeField()
    end_date=models.DateTimeField()
    host=models.ForeignKey(User, on_delete=models.CASCADE)
    image=models.ImageField(null=True,blank=True)
    prizes = models.CharField(max_length=500,null=True,blank=True)

    def __str__(self):
        return self.name

    def avg_rating(self):
        ratings=self.rating_set.all().values_list('rating')
        total=0
        for rating in ratings:
            total+=rating[0]

        avg=total//(len(ratings))
        return avg
    

class Rating(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    event=models.ForeignKey(Event,on_delete=models.CASCADE)
    rating=models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(5)])

    def __str__(self):
        return self.user.email + ' for '+self.event.name
