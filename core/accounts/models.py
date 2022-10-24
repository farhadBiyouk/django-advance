from email.policy import default
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator
from django.db.models.signals import  post_save
from django.dispatch import  receiver



class UserManager(BaseUserManager):
    def create_user(self,email, password=None):
        if not email:
            raise ValueError("You must to import Email address")

        user = self.model(
            email = self.normalize_email(email),)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email, password=None):
        user = self.create_user(
            email = self.normalize_email(email),
        )
        user.is_staff = True
        user.is_superuser = True
        user.is_active =True
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser ,PermissionsMixin):
    email = models.EmailField(max_length=254, unique=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(default=False)

    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    
    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
        

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=254)
    last_name = models.CharField(max_length=254)
    image = models.ImageField(upload_to='user_profile/', blank=True, null=True)
    description = models.TextField()

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    if kwargs['created']:
        Profile.objects.create(user=instance)

