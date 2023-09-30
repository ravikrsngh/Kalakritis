from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
# Create your models here.



class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifier
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('Users must have an email address'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


def user_directory_path(instance,filename):
    return 'media/ProfilePictures/user_{0}/{1}'.format(instance.email, filename)

class CustomUser(AbstractUser):
    username = None
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(unique=True, max_length=254)
    temp_otp = models.CharField(max_length=4, default="0000")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"


user_address_choices = [
        ("1", "Home"),
        ("2", "Office"),
        ("3", "Others"),
]


class UserAddress(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    email = models.EmailField()
    country = models.CharField(max_length=30, default="India")
    state = models.CharField(max_length=30)
    address_line1 = models.CharField(max_length=120)
    city = models.CharField(max_length=30)
    zipcode = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=15)
    address_type = models.CharField(max_length=1, choices=user_address_choices, default="1")

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name = "User Address"
        verbose_name_plural = "User Addresses"


class RecentSearch(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="recent_searches")
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Recent Search"
        verbose_name_plural = "Recent Searches"


class Newsletter(models.Model):
    email = models.CharField(max_length=50,unique=True)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Newsletter"
        verbose_name_plural = "Newsletters"


class TemperaryOTP(models.Model):
    email = models.CharField(max_length=50)
    temp_otp = models.CharField(max_length=4)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Temperary OTP"
        verbose_name_plural = "Temperary OTP"
