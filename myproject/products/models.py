from django.db import models
from django.utils import timezone
import os
import string
import secrets
# Create your models here.
def id_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(size))

def path_and_rename(instance, filename):
    upload_to = 'uploads/products/'
    ext = filename.split('.')[-1]
    # get filename
    if instance.pk:
        filename = '{}.{}'.format(id_generator(), ext)
    else:
        # set filename as random string
        filename = '{}.{}'.format(id_generator(), ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)

class Products(models.Model):
    class Meta:
        db_table = 'products'

    id          = models.AutoField(primary_key=True,max_length=11)
    name        = models.CharField(max_length=80)
    code        = models.CharField(max_length=50, unique=True)
    photo       = models.ImageField(upload_to=path_and_rename)
    description = models.CharField(max_length=191, blank=True, null=True)
    stock       = models.CharField(max_length=80)
    price       = models.CharField(max_length=191)
    categories  = models.ForeignKey('Category',related_name='to_products',on_delete=models.CASCADE)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return self.name

class Category(models.Model):
    class Meta:
        db_table = 'categories'

    id          = models.AutoField(primary_key=True,max_length=11)
    name        = models.CharField(max_length=80,unique=True)
    description = models.CharField(max_length=191, blank=True, null=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
