from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=255, unique=True)
    image = models.ImageField(upload_to='img/items/')
    weight = models.DecimalField(max_digits=3, decimal_places=1)
    width = models.PositiveSmallIntegerField()
    height = models.PositiveSmallIntegerField()

    def __str__(self):
        return f'Item: {self.name}. Buyer Price: {self.price.buyer}. Seller Price: {self.price.seller}'  # noqa


class Price(models.Model):
    buyer = models.PositiveIntegerField()
    seller = models.PositiveIntegerField()

    item = models.OneToOneField(Item, on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self):
        return f'Item: {self.item.name}. Buyer Price: {self.buyer}. Seller Price: {self.seller}'


class Entity(models.Model):
    name = models.CharField(max_length=255)
    balance = models.PositiveIntegerField()

    class Meta:
        abstract = True


class Buyer(Entity):
    image = models.ImageField(upload_to='img/buyers/', default='static/img/buyer.jpg')

    def __str__(self):
        return f'ID: {self.id}. Name: {self.name}'  # noqa


class Seller(Entity):
    image = models.ImageField(upload_to='img/sellers/', default='static/img/seller.jpg')

    def __str__(self):
        return f'ID: {self.id}. Name: {self.name}'  # noqa


class Inventory(models.Model):
    quantity = models.PositiveIntegerField()

    item = models.OneToOneField(Item, on_delete=models.CASCADE, null=False, blank=False)

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
