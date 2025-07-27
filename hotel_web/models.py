from django.db import models
from login.models import Userdata
from django.utils import timezone
from datetime import datetime

class Contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=12)
    peoples = models.PositiveIntegerField(default=1)
    date = models.DateField(default=datetime.now().strftime("%d:%m:%Y"))
    time = models.TimeField(default=datetime.now().strftime("%H:%M:%S"))
    table = models.IntegerField(default=1)

    def __str__(self):
        return self.name

class Product(models.Model):
    STATUS_CHOICES = [("AVAILABLE", "available"),
              ("UNAVAILABLE", "unavailable")]
    product_id = models.AutoField
    product_name = models.CharField(max_length=200)
    disc = models.TextField(max_length=80)
    price = models.DecimalField(max_digits = 10, decimal_places=2)
    image = models.ImageField(upload_to='products/images')
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default="AVAILABLE")

    def __str__(self):
        return self.product_name

class Cart(models.Model):
    user = models.ForeignKey(Userdata, on_delete=models.CASCADE)
    
    def __str__(self):
        return f' Cart of {self.user.username}'

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return f'{self.quantity} of {self.product.product_name} in {self.cart.user.username}\' s cart' 
    
    def total_price(self):
        return self.product.price * self.quantity

class Order(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('ACCEPTED', 'Accepted'),
        ('REJECTED', 'Rejected'),
        ('DELIVERED', 'Delivered'),
    ]
    
    user = models.ForeignKey(Userdata, on_delete=models.CASCADE)
    items = models.CharField(max_length=1000, default=list)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'Order of {self.user.first_name} {self.user.last_name}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f'{self.quantity} of {self.product.product_name}'
    
    @property
    def total_price(self):
        return self.price * self.quantity

class TempStatus(models.Model):
    user = models.ForeignKey(Userdata, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, default='PENDING')

class Delivery(models.Model):
    user = models.ForeignKey(Userdata, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    delivered = models.BooleanField(default=False)
    delivered_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'Delivered Order of {self.user.first_name} {self.user.last_name}'