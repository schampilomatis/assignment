import datetime
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,PermissionsMixin
from django.contrib.gis.db import models
from django.contrib.auth import get_user_model


class CustomUserManager(BaseUserManager):

    def create_user(self, username, email, password=None):
        self._create_user(username, email, password, False, False)

    def create_superuser(self, username, password):
        self._create_user(username, username, password, True, True)

    def _create_user(self, username, email, password,
                     is_staff, is_superuser):
        """
        Creates and saves a User with the given email and password.
        """
        now = datetime.datetime.now()
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        User = get_user_model()
        user = User(username=username, email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now)
        user.set_password(password)
        user.save(using=self._db)

        return user


class UserWithEmail(AbstractBaseUser, PermissionsMixin):
    username = models.TextField('username', max_length=255, null=False, blank=False, unique=True, db_index=True)
    email = models.EmailField('email', null=True, blank=True , unique=True, db_index=True)
    name = models.CharField('name', max_length=255 , null=True, blank=True )
    lastname = models.CharField('lastname', max_length=255, null=True, blank=True )
    provider_id = models.TextField('provider_id', max_length=255, null=True, blank=True,)
    provider = models.TextField('provider', max_length=255, null=True, blank=True)
    active = models.BooleanField('active', default=True)
    is_active = models.BooleanField('is_active', default=True)
    is_staff = models.BooleanField('is_staff', default=False)
    date_joined = models.DateTimeField('date_joined', null=True, blank=True, auto_now_add=True)
    objects = CustomUserManager()
    USERNAME_FIELD = 'username'

    def get_full_name(self):
        return '{} {}'.format(self.name, self.lastname)

    def get_short_name(self):
        return self.name or self.username

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
