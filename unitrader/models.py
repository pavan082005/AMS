from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    roll_number = models.CharField(max_length=20, unique=True)
    date_of_birth = models.DateField()
    age = models.IntegerField()
    date_joined = models.DateField(auto_now_add=True)
    ph_number = models.CharField(max_length=15)

    def __str__(self):
        return self.user.username

from django.db import models
from django.contrib.auth.models import User

class Item(models.Model):
    item_title = models.CharField(max_length=100)
    item_description = models.TextField()
    item_tags = models.CharField(max_length=255, blank=True, null=True)  # Tags can be optional
    item_age = models.IntegerField(null=True, blank=True)  # Age can be optional
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    item_image = models.ImageField(upload_to='item_images/', blank=True, null=True)  # File upload field
    
    quantity = models.IntegerField(default=1)
    
    seller = models.ForeignKey(User, on_delete=models.CASCADE)  # Reference to the seller
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Status for the item's availability
    status = models.CharField(
        max_length=20, 
        choices=[('available', 'Available'), ('sold', 'Sold')], 
        default='available'
    )

    # New fields for bidding
    highest_bid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    highest_bidder = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='highest_bidder')

    def __str__(self):
        return self.item_title

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)  # To track read/unread status

    def __str__(self):
        return f'Message from {self.sender.username} to {self.recipient.username}'