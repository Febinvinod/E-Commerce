
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Custom User Manager
class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None, is_vendor=False):
        if not email:
            raise ValueError("Users must have an email address")
        user = self.model(
            email=self.normalize_email(email),
            name=name,
            is_vendor=is_vendor
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None):
        user = self.create_user(email, name, password)
        user.is_staff = True
        user.save(using=self._db)
        return user


# User Model
class User(AbstractBaseUser, PermissionsMixin):  # Added PermissionsMixin
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    is_vendor = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)  # Required for admin
    is_active = models.BooleanField(default=True)  # Required for admin

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        """Check if the user has a specific permission."""
        return True

    def has_module_perms(self, app_label):
        """Check if the user has permissions to view the app."""
        return True



# Vendor Model
class Vendor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="vendor_profile")
    company_name = models.CharField(max_length=100)

    def __str__(self):
        return self.company_name
