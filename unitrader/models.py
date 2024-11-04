from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from datetime import timedelta

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    roll_number = models.CharField(max_length=20, unique=True)
    date_of_birth = models.DateField()
    age = models.IntegerField()
    date_joined = models.DateField(auto_now_add=True)
    ph_number = models.CharField(max_length=15)
    coins = models.IntegerField(default=500)

    def __str__(self):
        return self.user.username

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

    # Bidding fields
    highest_bid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    highest_bidder = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='highest_bidder')
    bidding_end_time = models.DateTimeField()  # Set this when the item is created

    # Status for the item's availability
    status = models.CharField(
        max_length=20, 
        choices=[('available', 'Available'), ('sold', 'Sold')], 
        default='available'
    )

    def __str__(self):
        return self.item_title

    def save(self, *args, **kwargs):
        """Automatically set bidding_end_time when the item is created."""
        if not self.id:  # Check if this is a new item
            self.bidding_end_time = timezone.now() + timedelta(weeks=1)  # Bidding lasts for one week
        super().save(*args, **kwargs)

    def finalize_auction(self):
        """Finalizes the auction and sells the item to the highest bidder if the auction time has ended."""
        if timezone.now() >= self.bidding_end_time:
            if self.highest_bidder:
                # Mark item as sold
                self.status = 'sold'
                self.quantity = 0  # Set quantity to zero to indicate it has been sold
                self.save()  # Save the item status as sold

                all_bidders = Bid.objects.filter(item=self).values_list('user', flat=True)  # Get all users who placed bids
                for bidder_id in all_bidders:
                    bidder = User.objects.get(id=bidder_id)
                    if bidder != self.highest_bidder:
                        profile = bidder.profile
                        total_bid_amount = Bid.objects.filter(item=self, user=bidder).aggregate(models.Sum('amount'))['amount__sum'] or 0
                        profile.coins += total_bid_amount
                        profile.save()
            else:
                self.status = 'available'  # If there were no bids, keep item available
                self.save()


class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} bid ${self.amount} on {self.item.item_title}"
    
class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)  # To track read/unread status

    def __str__(self):
        return f'Message from {self.sender.username} to {self.recipient.username}'
