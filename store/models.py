from django.db import models
from django.contrib.auth.models import User
import uuid
import qrcode
from io import BytesIO
from django.core.files import File

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.IntegerField()
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='uploads/products/')
    is_sale = models.BooleanField(default=False)
    sale_price = models.IntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Packed', 'Packed'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=100)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    city = models.CharField(max_length=50)
    pincode = models.CharField(max_length=10)
    total_amount = models.IntegerField()
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    # --- TRACKING & SHIPROCKET FIELDS ---
    order_id = models.CharField(max_length=50, unique=True, blank=True)
    awb_code = models.CharField(max_length=100, blank=True, null=True)  # Shiprocket Tracking No
    courier_name = models.CharField(max_length=100, blank=True, null=True)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)

    def save(self, *args, **kwargs):
        # 1. Unique Order ID generate karna
        if not self.order_id:
            self.order_id = str(uuid.uuid4()).split('-')[0].upper()
        
        # 2. QR Code Generate karna (Jo parcel par lagega)
        if not self.qr_code:
            qr_data = f"Order: {self.order_id} | Amt: {self.total_amount}"
            qr_img = qrcode.make(qr_data)
            buffer = BytesIO()
            qr_img.save(buffer, format="PNG")
            fname = f'qr_{self.order_id}.png'
            self.qr_code.save(fname, File(buffer), save=False)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order #{self.order_id}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()
    
    from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# --- USER PROFILE (Phone & Seller Support) ---
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True, unique=True)
    is_seller = models.BooleanField(default=False) # Future me seller banane ke liye
    
    def __str__(self):
        return self.user.username

# Jab naya User bane, to automatic Profile bhi ban jaye
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()