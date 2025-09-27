from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create a profile when a user is created"""
    if created:
        Profile.objects.create(
            user=instance,
            first_name=instance.first_name or '',
            last_name=instance.last_name or '',
            email=instance.email or ''
        )


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Save the profile when user is saved"""
    if hasattr(instance, 'profile'):
        instance.profile.save()