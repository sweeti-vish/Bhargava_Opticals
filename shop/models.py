from django.contrib.auth.models import User
from datetime import timedelta
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from decimal import Decimal

class Brand(models.Model):
    name = models.CharField(max_length=60, unique=True)
    logo = models.ImageField(upload_to='brands/', blank=True)

    def __str__(self):
        return self.name

class Frame(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='frames')
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='frames/')
    description = models.TextField(blank=True)
    in_stock = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.brand.name} - {self.name}"

class Customer(models.Model):
    GENDER = [('M', 'Male'), ('F', 'Female'), ('O', 'Other')]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=10, unique=True)
    age = models.PositiveSmallIntegerField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER, blank=True)
    consent = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name} ({self.phone})"

class Order(models.Model):
    SHOPS = [('CC', 'Chandni Chowk'), ('CB', 'Chhipeti Bazar')]
    STATUS = [('PL', 'Placed'), ('RD', 'Ready for pickup'),
              ('PU', 'Picked up'), ('CN', 'Cancelled')]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    frame = models.ForeignKey(Frame, on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    shop = models.CharField(max_length=2, choices=SHOPS)
    status = models.CharField(max_length=2, choices=STATUS, default='PL')
    note = models.CharField(max_length=200, blank=True)
    advance_paid = models.BooleanField(default=False)
    ADVANCE_PERCENT = 50
    created = models.DateTimeField(auto_now_add=True)
    READY_DAYS = 2

    @property
    def ready_by(self):
        return self.created + timedelta(days=self.READY_DAYS)
    
    @property
    def advance_amount(self):
        return (self.price * self.ADVANCE_PERCENT / 100).quantize(Decimal('0.01'))

    @property
    def balance(self):
        return self.price - self.advance_amount
    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f"Order {self.id}: {self.frame} for {self.customer}"

class Review(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='review')
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)])
    feedback = models.TextField(max_length=400)
    approved = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    @property
    def stars(self):
        return '★' * self.rating + '☆' * (5 - self.rating)

    def __str__(self):
        return f"{self.rating}/5 for order {self.order_id}"