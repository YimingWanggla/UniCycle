from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# 1. Custom User Model (corresponding to the "User" table in the ER diagram)
class User(AbstractUser):
    # Override the default configuration, require an email address, and use the email address as the login username
    email = models.EmailField(unique=True, max_length=255)
    display_name = models.CharField(max_length=128, blank=True, null=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username'] # Fields that must be filled in when creating a superuser, in addition to the email address

    def __str__(self):
        return self.email

# 2. Classification Model (corresponding to the "Category" table in the ER diagram)
class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

# 3. Item List Model (corresponding to the "Listing" table in the ER diagram)
class Listing(models.Model):
    STATUS_CHOICES = [
        ('Available', 'Available'),
        ('Reserved', 'Reserved'),
        ('Sold', 'Sold'),
    ]

    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='listings')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='listings')
    title = models.CharField(max_length=64)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default='Available')
    pickup_location = models.CharField(max_length=128)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class ListingImage(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='listings/')
    
    def __str__(self):
        return f"Image for {self.listing.title}"

# 4. Item Image Model (corresponding to the ListingImage table in the ER diagram)
class ListingImage(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='listing_images/')

    def __str__(self):
        return f"Image for {self.listing.title}"

# 5. Message Model (corresponding to the "Message" table in the ER diagram)
class Message(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.email} about {self.listing.title}"

# 6. Favorites Model (corresponding to the "Favourite" table in the ER diagram)
class Favourite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favourites')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='favourited_by')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'listing') # Ensure that a user can only add an item to their favorites once

# 7. Report Model (corresponding to the "Report" table in the ER diagram)
class Report(models.Model):
    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reports_made')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='reports_received')
    reason = models.TextField()
    created = models.DateTimeField(auto_now_add=True)