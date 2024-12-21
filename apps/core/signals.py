from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Price, Seller


@receiver(post_delete, sender=Price)
def delete_related_item(sender, instance, **kwargs):
    if instance.item:
        instance.item.delete()


@receiver(post_delete, sender=Seller)
def delete_related_buyer(sender, instance, **kwargs):
    if instance.buyer:
        instance.buyer.delete()
