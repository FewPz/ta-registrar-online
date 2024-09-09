from django.db import models
from django.contrib.auth.hashers import make_password, is_password_usable, check_password
from django.utils import timezone

# Create your models here.
class User(models.Model):
    
    class UserManager(models.Manager):
        def get_queryset(self) -> models.QuerySet:
            return super().get_queryset().filter(deleted_at__isnull=True)

    class UserRole(models.TextChoices):
        STUDENT = "Student"
        STAFF = "Staff"
        FINANCE = "Finance"
        PROFESSOR = "Professor"

    username = models.CharField(max_length=150)
    password = models.CharField(max_length=255) # Must be encrypted password for security functionality
    first_name = models.TextField(default="-None-") # Some users may have longggg name -_-
    last_name = models.TextField(default="-None-") # Some users may have longggg name -_-
    role = models.CharField(max_length=100, choices=UserRole.choices, default=UserRole.STUDENT)
    last_login = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = UserManager()

    def __str__(self):
        return self.username
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def save(self, *args, **kwargs):
        # Only hash the password if it is not already hashed
        if not is_password_usable(self.password):
            self.password = make_password(self.password)
        super(User, self).save(*args, **kwargs)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    # Make sure that the object is not deleted
    def delete(self, *args, **kwargs):
        self.deleted_at = timezone.now()
        self.save()
