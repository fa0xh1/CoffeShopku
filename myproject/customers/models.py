from django.db import models
from accounts.models import User
from products.models import Products
# Create your models here.
class Customers(models.Model):

    class Meta:
        db_table = 'customers'

    id          = models.AutoField(primary_key=True,max_length=11)
    email       = models.EmailField(unique=True)
    name        = models.CharField(max_length=100)
    address     = models.TextField()
    phone       = models.CharField(max_length=15)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

class Orders(models.Model):

    class Meta:
        db_table = 'orders'

    id          = models.AutoField(primary_key=True,max_length=11)
    invoice     = models.CharField(unique=True, max_length=191)
    customer    = models.ForeignKey('Customers',on_delete=models.CASCADE)
    user        = models.ForeignKey('accounts.User',on_delete=models.CASCADE)
    total       = models.IntegerField()
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

class OrderDetails(models.Model):

    class Meta:
        db_table = 'order_details'

    id          = models.AutoField(primary_key=True,max_length=11)
    order       = models.ForeignKey('Orders', on_delete=models.CASCADE)
    product     = models.ForeignKey('products.Products', on_delete=models.CASCADE)
    qty         = models.IntegerField()
    price       = models.IntegerField()
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)