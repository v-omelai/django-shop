from django.db import transaction
from django.urls import reverse
from drf_extra_fields.fields import Base64ImageField
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from apps.core.exceptions import TransactionException
from apps.core.helpers import Helper
from apps.core.models import Seller, Buyer, SellerInventory, Goal, Transaction, BuyerInventory


class CreateSellerSerializer(serializers.ModelSerializer):
    link = serializers.SerializerMethodField()

    class Meta:
        model = Seller
        fields = ['id', 'link']
        read_only_fields = ['id', 'link']

    @extend_schema_field(serializers.CharField)
    def get_link(self, instance):  # noqa
        return reverse('game', kwargs={'seller': instance.id})

    def save(self):
        with transaction.atomic():
            # Initiate a buyer
            buyer = Buyer.objects.create(name='Vitalii Omelai')  # noqa

            # Initiate a seller
            goal = Goal.objects.get(difficulty=1)  # noqa
            seller = self.instance = Seller.objects.create(name='Player', balance=0, buyer=buyer, goal=goal)  # noqa

            # Create inventories
            Helper.Inventory.create(buyer, seller, goal)

        return self.instance


class UpdateSellerSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Seller
        fields = ['id', 'name', 'image']
        read_only_fields = ['id']
        extra_kwargs = {
            'name': {'required': False},
            'image': {'required': False},
        }


class ItemSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    quantity = serializers.IntegerField(min_value=1, default=1)


class EntitySerializer(serializers.Serializer):
    buyer = ItemSerializer(many=True, required=False)
    seller = ItemSerializer(many=True, required=False)


class CreateTransactionSerializer(serializers.ModelSerializer):
    items = EntitySerializer(write_only=True)
    processed = serializers.SerializerMethodField()
    link = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = ['buyer', 'seller', 'items', 'processed', 'link']
        read_only_fields = ['processed', 'link']

    @extend_schema_field(serializers.BooleanField)
    def get_processed(self, instance):  # noqa
        return True if instance.status == 'completed' else False

    @extend_schema_field(serializers.CharField)
    def get_link(self, instance):  # noqa
        return reverse('congratulations') if instance.seller.goal is None else None

    def save(self):
        validated_data = self.validated_data
        buyer = validated_data.get('buyer')
        seller = validated_data.get('seller')
        items = validated_data.get('items', {})
        t = self.instance = Transaction.objects.create(buyer=buyer, seller=seller)  # noqa

        try:
            # Game over check
            if seller.goal is None:
                raise TransactionException

            with transaction.atomic():
                # Player buys
                for dictionary in items.get('buyer', []):
                    item, quantity = Helper.Item.get(dictionary)
                    if BuyerInventory.objects.filter(  # noqa
                            buyer=buyer, item=item, quantity__gte=quantity
                    ).exists():
                        seller.balance -= item.price.seller * quantity
                    else:
                        raise TransactionException
                # Player sells
                for dictionary in items.get('seller', []):
                    item, quantity = Helper.Item.get(dictionary)
                    if SellerInventory.objects.filter(  # noqa
                            seller=seller, item=item, quantity__gte=quantity
                    ).exists():
                        seller.balance += item.price.buyer * quantity
                    else:
                        raise TransactionException

                if seller.balance == seller.goal.balance:
                    # Move player
                    goal = seller.goal = Goal.objects.filter(  # noqa
                        difficulty__gt=seller.goal.difficulty
                    ).order_by('difficulty').first()

                    # Delete inventories
                    Helper.Inventory.delete(buyer, seller)

                    # Create inventories
                    if goal:
                        Helper.Inventory.create(buyer, seller, goal)

                    seller.save()
                else:
                    raise TransactionException
        except Exception as e:
            t.status = 'canceled'
            raise e
        else:
            t.status = 'completed'
        finally:
            t.save()

        return self.instance
