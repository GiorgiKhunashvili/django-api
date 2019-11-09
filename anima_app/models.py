from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
# Create your models here.


class UserAccountManager(BaseUserManager):
    """Creating Manager for our custom database"""
    def create_user(self, email, username, name,  password=None):
        """this function creates users and saves in database"""
        if not email:
            raise ValueError("users must have email!")

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, name=name)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, username, name, password):
        """creating super users"""
        user = self.create_user(email, username, name, password)
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class UserAccount(AbstractBaseUser, PermissionsMixin):
    """Creating custom database for users"""
    email = models.EmailField(max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=30)
    # date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True, null=True, blank=True)
    # last_login = models.DateTimeField(verbose_name='last login', auto_now=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'name']

    objects = UserAccountManager()

    def get_full_name(self):
        """geting full name for django"""
        return self.name

    def get_short_name(self):
        """geting short name for django"""
        return self.name

    def __str__(self):
        """string representation"""
        return self.email


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
