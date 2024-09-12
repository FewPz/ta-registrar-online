from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password, is_password_usable

class UserManager(BaseUserManager):
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().filter(deleted_at__isnull=True)

    def create_user(self, username, password=None, **extra_fields):
        """Creates and saves a regular user."""
        if not username:
            raise ValueError('The Username must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=255)
    first_name = models.TextField(default="-None-")
    last_name = models.TextField(default="-None-")
    last_login = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    
    # Adding related_name to avoid clashes with the default User model
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='taauth_user_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='taauth_user_permissions_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def set_password(self, raw_password):
        """Hashes the password."""
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        """Verifies the password."""
        return check_password(raw_password, self.password)

    def save(self, *args, **kwargs):
        """Override save to ensure the password is hashed."""
        if not is_password_usable(self.password):
            self.password = make_password(self.password)
        super(User, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """Soft delete the user by setting deleted_at."""
        self.deleted_at = timezone.now()
        self.save()
