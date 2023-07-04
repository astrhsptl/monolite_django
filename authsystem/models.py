import uuid

from django.db import models
from django.urls import reverse_lazy
from django.contrib.auth.models import (
	AbstractBaseUser, BaseUserManager,
)

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, username, email, password, avatar=None):
        print(self.model)
        user = self.model(email=self.normalize_email(email))
        user.username = username
        user.avatar = avatar
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password, avatar=None):
        user = self.create_user(username, email, password, avatar)
        user.is_superuser = True
        user.is_staff = True
        user.set_password(password)
        user.save()

        return user

class User(AbstractBaseUser):
    id = models.UUIDField(
        primary_key=True,
        db_index=True,
        default=uuid.uuid4,
        editable=False)
    email = models.EmailField('email adress', max_length=256, unique=True,)
    username = models.CharField(max_length=256, unique=True)
    created = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # Auth settings
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'username'
    ]

    objects = UserManager()

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    def __str__(self):
        return self.email

    def get_absolute_url(self,):
        return reverse_lazy('user_detail', kwargs={'pk': self.id})

    class Meta:
        verbose_name = ("User")
        verbose_name_plural = ("Users")
        indexes = [
            models.Index(fields=['id'], name='id_index'),
        ]