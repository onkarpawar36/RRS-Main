from django.contrib import admin
from .models import Room, RoomImage, RoomBookmark, RoomReview


class RoomImageInline(admin.TabularInline):
    model = RoomImage
    extra = 1
    fields = ['image', 'caption', 'is_main']


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['title', 'owner', 'category', 'room_type', 'price', 'city', 'is_available', 'created_at']
    list_filter = ['category', 'room_type', 'is_available', 'featured', 'city', 'created_at']
    search_fields = ['title', 'description', 'address', 'city', 'owner__username']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [RoomImageInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'owner', 'category', 'room_type')
        }),
        ('Pricing & Location', {
            'fields': ('price', 'address', 'city', 'state', 'pincode')
        }),
        ('Room Details', {
            'fields': ('area_sqft', 'bedrooms', 'bathrooms', 'max_occupancy')
        }),
        ('Amenities', {
            'fields': ('wifi', 'parking', 'ac', 'laundry', 'kitchen', 'gym', 'swimming_pool', 'security'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_available', 'featured')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(RoomImage)
class RoomImageAdmin(admin.ModelAdmin):
    list_display = ['room', 'caption', 'is_main', 'created_at']
    list_filter = ['is_main', 'created_at']
    search_fields = ['room__title', 'caption']


@admin.register(RoomBookmark)
class RoomBookmarkAdmin(admin.ModelAdmin):
    list_display = ['user', 'room', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'room__title']


@admin.register(RoomReview)
class RoomReviewAdmin(admin.ModelAdmin):
    list_display = ['room', 'user', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['room__title', 'user__username', 'comment']
    readonly_fields = ['created_at']
