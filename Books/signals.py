from django.db.models.signals import post_save
from users.models import CustomUser
from django.dispatch import receiver
from .models import Shelf

@receiver(post_save, sender=CustomUser)
def create_default_shelves(sender, instance, created, **kwargs):
    if created:
        # Create the "want to read" shelf
        Shelf.objects.create(name="Want to Read", user=instance)

        # Create the "currently reading" shelf
        Shelf.objects.create(name='Currently reading', user=instance)
