import uuid

from django.db import models
from django_cleanup import cleanup


class Timestamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


@cleanup.ignore
class Item(Timestamp):
    name = models.CharField(max_length=255, unique=True)
    image = models.ImageField(upload_to='items/')

    def __str__(self):
        return f'Item: {self.name}. Buyer Price: {self.price.buyer}. Seller Price: {self.price.seller}'  # noqa


class Price(Timestamp):
    buyer = models.PositiveIntegerField()
    seller = models.PositiveIntegerField()

    item = models.OneToOneField(Item, on_delete=models.CASCADE, null=True, blank=False)

    def __str__(self):
        return f'Item: {self.item.name}. Buyer Price: {self.buyer}. Seller Price: {self.seller}'


class Goal(Timestamp):
    RANK_CHOICES = [
        ('rookie', 'Rookie'),
        ('experienced', 'Experienced'),
        ('professional', 'Professional'),
        ('veteran', 'Veteran'),
        ('expert', 'Expert'),
    ]
    difficulty = models.PositiveIntegerField()
    balance = models.PositiveIntegerField()
    rank = models.CharField(max_length=20, choices=RANK_CHOICES, default='rookie')

    def __str__(self):
        return f'Difficulty: {self.difficulty}. Balance: {self.balance}'


class Entity(Timestamp):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=24)
    balance = models.PositiveIntegerField()

    class Meta:
        abstract = True


# Developer
class Buyer(Entity):
    image = models.ImageField(upload_to='buyers/', default='buyers/profile.jpg')

    def __str__(self):
        return f'ID: {self.id}. Name: {self.name}'  # noqa


# Player
class Seller(Entity):
    image = models.ImageField(upload_to='sellers/', default='sellers/profile.png')

    buyer = models.OneToOneField(Buyer, on_delete=models.CASCADE, null=False, blank=False, related_name='seller')
    goal = models.ForeignKey(Goal, on_delete=models.PROTECT, null=True, blank=True, related_name='sellers')

    def __str__(self):
        return f'ID: {self.id}. Name: {self.name}'  # noqa


class Inventory(Timestamp):
    quantity = models.PositiveIntegerField()

    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=False, blank=False)

    class Meta:
        abstract = True


class BuyerInventory(Inventory):
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE, null=False, blank=False, related_name='inventory')

    class Meta:
        verbose_name = 'buyer inventory'
        verbose_name_plural = 'buyer inventories'

    def __str__(self):
        return (
            f'Item: {self.item.name}. '
            f'Quantity: {self.quantity}. '
            f'Buyer ID: {self.buyer.id}. '  # noqa
            f'Buyer Name: {self.buyer.name}'
        )


class SellerInventory(Inventory):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, null=False, blank=False, related_name='inventory')

    class Meta:
        verbose_name = 'seller inventory'
        verbose_name_plural = 'seller inventories'

    def __str__(self):
        return (
            f'Item: {self.item.name}. '
            f'Quantity: {self.quantity}. '
            f'Seller ID: {self.seller.id}. '  # noqa
            f'Seller Name: {self.seller.name}'
        )


class Transaction(Timestamp):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]

    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE, related_name='transactions')
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='transactions')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f'ID: {self.id}. Status: {self.status.capitalize()}'  # noqa
