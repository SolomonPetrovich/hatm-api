from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin)

from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken


class UserManager(BaseUserManager):

    def create_user(self, email):
        if email is None:
            raise TypeError('Users should have a Email')

        user = self.model(email=self.normalize_email(email))
        user.save()
        return user

    def create_superuser(self, email,  password=None):
        if password is None:
            raise TypeError('Password should not be none')

        user = self.create_user(email)
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


AUTH_PROVIDERS = {'google': 'google', 'apple': 'apple'}


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = None
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    nickname = models.CharField(max_length=150, default=None, null=True)
    active_hatms = models.PositiveIntegerField(default=0)
    hatms_created = models.PositiveIntegerField(default=0)
    auth_provider = models.CharField(max_length=150)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.email

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        access = AccessToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(access),
            'acces_expires_in': str(access.lifetime.total_seconds()),
            'refresh_expires_in': str(refresh.lifetime.total_seconds())
        }
