from django.contrib.auth.models import (
    BaseUserManager
)
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserRoles(models.TextChoices):
    USER = "user", _('User')
    ADMIN = "admin", _('Admin')


class UserManager(BaseUserManager):
    """
    User model manager where email is the unique identifier
    for authentication instead of username
    """
    def create_user(self, email, first_name, last_name, phone, role=UserRoles.USER, password=None):
        """
        Creates and saves a User with the given email and password
        """
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            role=role,
        )
        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, first_name, last_name, phone, password=None):
        """
        Creates and saves a Superuser with the given email and password
        """
        user = self.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            password=password,
            role=UserRoles.ADMIN,
        )

        user.save(using=self._db)
        return user
