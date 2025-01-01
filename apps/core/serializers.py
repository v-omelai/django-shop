from django.db import transaction
from django.urls import reverse
from drf_extra_fields.fields import Base64ImageField
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from apps.core.exceptions import TransactionException
from apps.core.models import Seller, Buyer, SellerInventory, Goal, Transaction, Item, BuyerInventory


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

            # Create items
            exec(goal.code)

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
    OPERATION_CHOICES = [
        ('buy', 'Buy'),
        ('sell', 'Sell'),
    ]

    name = serializers.CharField(max_length=255)
    quantity = serializers.IntegerField(min_value=1, default=1)
    operation = serializers.ChoiceField(choices=OPERATION_CHOICES)


class CreateTransactionSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True, write_only=True)
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
        items = validated_data.get('items', [])
        t = self.instance = Transaction.objects.create(buyer=buyer, seller=seller)  # noqa

        try:
            if seller.goal is None:
                raise TransactionException

            with transaction.atomic():
                for dictionary in items:
                    name = dictionary.get('name', '').capitalize()
                    quantity = dictionary.get('quantity', 1)
                    operation = dictionary.get('operation')

                    item = get_object_or_404(Item, name=name)

                    match operation:
                        case 'buy':
                            if BuyerInventory.objects.filter(  # noqa
                                    buyer=buyer, item=item, quantity__gte=quantity
                            ).exists():
                                seller.balance -= item.price.seller * quantity
                            else:
                                raise TransactionException
                        case 'sell':
                            if SellerInventory.objects.filter(  # noqa
                                    seller=seller, item=item, quantity__gte=quantity
                            ).exists():
                                seller.balance += item.price.buyer * quantity
                            else:
                                raise TransactionException

                if seller.balance == seller.goal.balance:
                    goal = seller.goal = Goal.objects.filter(  # noqa
                        difficulty__gt=seller.goal.difficulty
                    ).order_by('difficulty').first()

                    BuyerInventory.objects.filter(buyer=buyer).delete()  # noqa
                    SellerInventory.objects.filter(seller=seller).delete()  # noqa

                    if goal:
                        exec(goal.code)

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
