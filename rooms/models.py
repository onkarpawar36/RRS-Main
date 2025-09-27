from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image
import os


class Room(models.Model):
    ROOM_CATEGORIES = [
        ('boys', 'Boys'),
        ('girls', 'Girls'),
        ('family', 'Family'),
    ]
    
    ROOM_TYPES = [
        ('pg', 'PG (Paying Guest)'),
        ('flat', 'Flat'),
        ('hostel', 'Hostel'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rooms')
    category = models.CharField(max_length=10, choices=ROOM_CATEGORIES)
    room_type = models.CharField(max_length=10, choices=ROOM_TYPES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    security_deposit = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="Security deposit amount")
    address = models.TextField(max_length=500)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    
    # Room features
    area_sqft = models.PositiveIntegerField(help_text="Area in square feet")
    bedrooms = models.PositiveIntegerField(default=1)
    bathrooms = models.PositiveIntegerField(default=1)
    max_occupancy = models.PositiveIntegerField(default=1)
    
    # Availability
    available_from = models.DateField(null=True, blank=True, help_text="Date from when the room is available")
    floor = models.CharField(max_length=20, blank=True, null=True, help_text="Floor number (e.g., Ground, 1st, 2nd)")
    
    # Amenities
    wifi = models.BooleanField(default=False)
    parking = models.BooleanField(default=False)
    ac = models.BooleanField(default=False)
    laundry = models.BooleanField(default=False)
    kitchen = models.BooleanField(default=False)
    food_included = models.BooleanField(default=False)
    gym = models.BooleanField(default=False)
    swimming_pool = models.BooleanField(default=False)
    security = models.BooleanField(default=False)
    
    # Status
    is_available = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('rooms:room_detail', kwargs={'pk': self.pk})
    
    @property
    def main_image(self):
        """Return the first image of the room"""
        first_image = self.images.first()
        if first_image:
            return first_image.image.url
        return '/static/images/default_room.svg'
    
    @property
    def amenity_list(self):
        """Return list of available amenities"""
        amenities = []
        if self.wifi: amenities.append('WiFi')
        if self.parking: amenities.append('Parking')
        if self.ac: amenities.append('AC')
        if self.laundry: amenities.append('Laundry')
        if self.kitchen: amenities.append('Kitchen')
        if self.food_included: amenities.append('Food Included')
        if self.gym: amenities.append('Gym')
        if self.swimming_pool: amenities.append('Swimming Pool')
        if self.security: amenities.append('Security')
        return amenities
    
    @property
    def amenity_count(self):
        return len(self.amenity_list)


class RoomImage(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='room_pics/')
    caption = models.CharField(max_length=200, blank=True)
    is_main = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-is_main', 'created_at']
        
    def __str__(self):
        return f"Image for {self.room.title}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        if self.image and hasattr(self.image, 'path'):
            # Resize image if it's too large
            img = Image.open(self.image.path)
            if img.height > 800 or img.width > 800:
                output_size = (800, 800)
                img.thumbnail(output_size)
                img.save(self.image.path)


class RoomBookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'room')
        
    def __str__(self):
        return f"{self.user.username} bookmarked {self.room.title}"


class RoomReview(models.Model):
    RATING_CHOICES = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]
    
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('room', 'user')
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.user.username} rated {self.room.title} - {self.rating} stars"


class RoomReport(models.Model):
    REPORT_REASONS = [
        ('inappropriate', 'Inappropriate Content'),
        ('fake', 'Fake Listing'),
        ('spam', 'Spam'),
        ('misleading', 'Misleading Information'),
        ('scam', 'Potential Scam'),
        ('duplicate', 'Duplicate Listing'),
        ('inappropriate_images', 'Inappropriate Images'),
        ('wrong_location', 'Wrong Location'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('investigating', 'Under Investigation'),
        ('resolved', 'Resolved'),
        ('dismissed', 'Dismissed'),
    ]
    
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='reports')
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submitted_reports')
    reason = models.CharField(max_length=20, choices=REPORT_REASONS)
    description = models.TextField(help_text="Please provide details about the issue")
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    
    # Admin fields
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_reports')
    admin_notes = models.TextField(blank=True, help_text="Internal notes for admin use")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('room', 'reporter')  # Prevent duplicate reports from same user
        ordering = ['-created_at']
        
    def __str__(self):
        return f"Report by {self.reporter.username} for {self.room.title} - {self.get_reason_display()}"
