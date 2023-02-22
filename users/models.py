from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token

class UserManagerCustom(UserManager):
    def create_user(self, email, password, **extra_fields):
        user = self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=150, null=False, blank=False, unique=True)
    first_name = models.CharField(max_length=100, null=False, blank=False)
    last_name = models.CharField(max_length=100, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = UserManagerCustom()
    USERNAME_FIELD = 'email'

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'

    class Meta:
        db_table = 'user'
        verbose_name_plural = 'users'

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_auth_token(sender, instance=None, created=False, **kwargs):
        if created:
            Token.objects.create(user=instance)