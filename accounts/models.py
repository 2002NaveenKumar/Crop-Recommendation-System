from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email = models.EmailField(verbose_name="email address", max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
    
class TestReport(models.Model):
    nitrogen = models.CharField(max_length=255)
    phosphorus = models.CharField(max_length=255)
    potassium = models.CharField(max_length=255)
    temperature = models.CharField(max_length=255)
    humidity = models.CharField(max_length=255)
    ph = models.CharField(max_length=255)
    rainfall = models.CharField(max_length=255)
    result = models.CharField(max_length=255)
    account_id = models.CharField(max_length=10,default=0)

    def __str__(self):
        return f"Test Report {self.id}"
