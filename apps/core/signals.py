from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Price, Seller, Item, Buyer


@receiver(post_delete, sender=Price)
def delete_related_item(sender, instance, **kwargs):
    try:
        instance.item.delete()
    except Item.DoesNotExist:  # noqa
        pass


@receiver(post_delete, sender=Seller)
def delete_related_buyer(sender, instance, **kwargs):
    try:
        instance.buyer.delete()
    except Buyer.DoesNotExist:  # noqa
        pass
