from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
class Category(models.Model):
    Category_name = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.Category_name


class Product(models.Model):
    product_id = models.AutoField # Make product_id the primary key
    product_name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    price = models.IntegerField(default=0)
    desc = models.CharField(max_length=500)
    pub_date = models.DateField()
    image = models.ImageField(upload_to="shop/images", default="")
    link = models.CharField(max_length=500, default="")

    def __str__(self):
        return self.product_name


class Contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50, default="")
    phone = models.CharField(max_length=50, default="")
    desc = models.CharField(max_length=5000)

    def __str__(self):
        return self.name


class Orders(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Link to User
    price = models.CharField(max_length=500, null=False, default='0')
    order_id = models.AutoField(primary_key=True)  # Auto increment primary key
    products = models.CharField(max_length=5000)
    fname = models.CharField(max_length=500)
    lname = models.CharField(max_length=50) 
    cn = models.CharField(max_length=500, default='None', blank=True)
    houseadd = models.CharField(max_length=500)
    apartment = models.CharField(max_length=500, default='None', blank=True)
    city = models.CharField(max_length=500)
    state = models.CharField(max_length=500)
    zip = models.CharField(max_length=500)
    phone = models.CharField(max_length=500)
    email = models.CharField(max_length=500)
    success_full = models.BooleanField(null=True, default=False)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
    order_date = models.DateField(default=timezone.now)  # Set default to current date
    def __str__(self):
        return f"{self.fname} - {self.status}"

class Review(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link review to the user
    title = models.CharField(max_length=200,default="No Way")  # Title of the review
    rating = models.IntegerField()  # Rating from 1 to 5
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review for {self.product.product_name} by {self.id}'