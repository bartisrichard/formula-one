from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin
from django.conf import settings


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Car(models.Model):
    name = models.CharField(max_length=255)
    enginesupplier = models.CharField(max_length=255)
    performance = models.IntegerField()
    wear = models.IntegerField()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class Rating(models.Model):
    name = models.CharField(max_length=255)
    overall = models.IntegerField()
    experience = models.IntegerField()
    racecraft = models.IntegerField()
    awareness = models.IntegerField()
    pace = models.IntegerField()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class Driver(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)
    salaryinmill = models.IntegerField()
    nationality = models.CharField(max_length=255)
    car = models.OneToOneField('Car', on_delete=models.CASCADE)
    rating = models.OneToOneField('Rating', on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Team(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)
    principal = models.CharField(max_length=255)
    income = models.IntegerField()
    drivers = models.OneToOneField('Driver', on_delete=models.CASCADE) #Itt tedd fel a kerdest

    def __str__(self):
        return self.title
