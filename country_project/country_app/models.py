from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
import uuid

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="customuser_groups",
        blank=True,
        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="customuser_user_permissions",
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    

class Country(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    country_code = models.CharField(max_length=255, unique=True)
    curr_symbol = models.CharField(max_length=255, unique=True)
    phone_code = models.CharField(max_length=255, unique=True)

    my_user = models.ForeignKey(CustomUser, related_name="Country_CustomUser", on_delete=models.CASCADE)

    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name

class State(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    state_code = models.CharField(max_length=255)
    gst_code = models.CharField(max_length=255)

    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    is_active = models.BooleanField(default=True)
  
    class Meta:
        unique_together = ('name', 'country')

    def __str__(self) -> str:
        return self.name
    
class City(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    city_code = models.CharField(max_length=255)
    phone_code = models.CharField(max_length=255)
    population = models.IntegerField(default=0)
    avg_age = models.DecimalField(default=0.0, decimal_places=2, max_digits=5)
    num_of_adult_males = models.IntegerField(default=0)
    num_of_adult_females = models.IntegerField(default=0)

    state = models.ForeignKey(State, on_delete=models.CASCADE)

    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('name', 'city_code', 'state')

    def __str__(self) -> str:
        return self.name



