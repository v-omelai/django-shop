from rest_framework.generics import get_object_or_404

from apps.core.models import BuyerInventory, SellerInventory, Item


class Helper:
    class Item:
        @staticmethod
        def get(dictionary):
            name = dictionary.get('name', '').capitalize()
            quantity = dictionary.get('quantity', 1)
            item = get_object_or_404(Item, name=name)
            return item, quantity

    class Inventory:
        @staticmethod
        def create(buyer, seller, goal):
            items = goal.json.get('items', {})
            buyer_ = items.get('buyer', [])
            seller_ = items.get('seller', [])

            for item in buyer_:
                name = item.get('name', '').capitalize()
                quantity = item.get('quantity', 1)
                i = Item.objects.get(name=name)  # noqa
                BuyerInventory.objects.create(buyer=buyer, quantity=quantity, item=i)  # noqa

            for item in seller_:
                name = item.get('name', '').capitalize()
                quantity = item.get('quantity', 1)
                i = Item.objects.get(name=name)  # noqa
                SellerInventory.objects.create(seller=seller, quantity=quantity, item=i)  # noqa

        @staticmethod
        def delete(buyer, seller):
            BuyerInventory.objects.filter(buyer=buyer).delete()  # noqa
            SellerInventory.objects.filter(seller=seller).delete()  # noqa
