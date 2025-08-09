from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from .manager import UserManager


class User(AbstractBaseUser):
    """
    Custom user model that extends Django's AbstractUser.
    This model can be used to add additional fields or methods in the future.
    """

    # You can add additional fields here if needed
    email = models.EmailField(unique=True, max_length=255)
    phone_number = models.CharField(max_length=11, unique=True)
    full_name = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email', 'full_name']

    def __str__(self):
        return f"{self.email}"

    def has_perm(self, perm, obj=None):
        """
        Returns True if the user has the specified permission.
        """
        return True
        # You can add additional logic here if needed, such as checking if the user is staff or# authenticated.

    def has_module_perms(self, app_label):
        """
        Returns True if the user has permission to view the specified app.
        """
        return True

    @property
    def is_staff(self):
        """
        Returns True if the user is a staff member.
        """
        return self.is_admin
