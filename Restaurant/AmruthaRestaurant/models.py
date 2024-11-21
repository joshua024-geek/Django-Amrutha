from django.db import models
import random
from django.utils import timezone

class BaseUser(models.Model):
    fullname = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)

    class Meta:
        abstract = True  # This model won't create a database table

    def __str__(self):
        return self.fullname

class User(BaseUser):
    # Additional fields specific to User can go here
    is_blocked = models.BooleanField(default=False)
    pass

class Admin(BaseUser):
    # Additional fields specific to Admin can go here
    pass
class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='menu_images/', blank=True, null=True)
    def __str__(self):
        return self.name
class Cart(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('purchased', 'Purchased'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey('MenuItem', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.user.email} - {self.product.name} - {self.quantity} - Total: {self.total_price} - Status: {self.status}"

class Order(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('card', 'Credit/Debit Card'),
        ('paypal', 'PayPal'),
        ('digital_wallet', 'Digital Wallet')
    ]
    DIGITAL_WALLET_CHOICES = [
        ('apple_pay', 'Apple Pay'),
        ('google_pay', 'Google Pay'),
        ('samsung_pay', 'Samsung Pay')
    ]
    ORDER_STATUS_CHOICES = [
        ('ordered', 'Ordered'),
        ('processing', 'Processing'),
        ('delivered', 'Delivered')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart_items = models.ManyToManyField(Cart, related_name='orders')
    order_number = models.CharField(max_length=20, unique=True, blank=True)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='ordered')
    address_line1 = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10)
    country = models.CharField(max_length=50)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    paypal_email = models.EmailField(blank=True, null=True)

    # Fields for Credit/Debit Card payment
    card_number = models.CharField(max_length=16, blank=True, null=True)
    card_expiry_date = models.CharField(max_length=5, blank=True, null=True)  # e.g., "MM/YY"
    card_cvv = models.CharField(max_length=3, blank=True, null=True)

    # Fields for Digital Wallet payment
    digital_wallet_type = models.CharField(max_length=20, choices=DIGITAL_WALLET_CHOICES, blank=True, null=True)

    special_instructions = models.TextField(blank=True, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = 'ORDER-' + str(random.randint(10000, 99999))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order #{self.order_number} by {self.user.fullname}"
class Notification(models.Model):
    order_number = models.CharField(max_length=20)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Links to the customer who placed the order
    notification = models.TextField()
    read_status = models.BooleanField(default=False)
    customer_read_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Notification for {self.user.fullname} - {self.order_number}"