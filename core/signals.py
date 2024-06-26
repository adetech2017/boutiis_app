from django.dispatch import receiver
from django.db.models.signals import post_save
from rest_framework_simplejwt.tokens import RefreshToken
#from django.contrib.auth import get_user_model
from .models import User



@receiver(post_save, sender=RefreshToken)
def update_user_online_status(sender, instance, created, **kwargs):
    if created:
        user = instance.user
        if user:
            user.is_online = True
            user.save(update_fields=['is_online'])
