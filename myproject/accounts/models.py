from __future__ import unicode_literals

from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from .managers import UserManager
import os
import string
import secrets
# Create your models here.
def id_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(size))

def path_and_rename(instance, filename):
    upload_to = 'uploads/avatar/'
    ext = filename.split('.')[-1]
    # get filename
    if instance.pk:
        filename = '{}.{}'.format(id_generator(), ext)
    else:
        # set filename as random string
        filename = '{}.{}'.format(id_generator(), ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)


class User(AbstractBaseUser, PermissionsMixin):
    
    email = models.EmailField(_('email'), unique=True)
    username = models.CharField(_('username'), max_length=45, unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=True)
    avatar = models.ImageField(upload_to=path_and_rename, null=True, blank=True)

    objects = UserManager()
    EMAIL_FIELD    = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def __str__(self):
        return self.username