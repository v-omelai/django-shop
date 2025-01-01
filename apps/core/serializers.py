from django.db import transaction
from django.urls import reverse
from drf_extra_fields.fields import Base64ImageField
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from .models import *


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
            buyer = Buyer.objects.create(name='Vitalii Omelai', balance=500)  # noqa

            # Initiate a seller
            goal = Goal.objects.get(difficulty=1)  # noqa
            seller = self.instance = Seller.objects.create(name='Player', balance=0, buyer=buyer, goal=goal)  # noqa

            # Add an apple
            apple = Item.objects.get(name='Apple')  # noqa
            SellerInventory.objects.create(seller=seller, quantity=1, item=apple)  # noqa

            # Add a carrot
            carrot = Item.objects.get(name='Carrot')  # noqa
            SellerInventory.objects.create(seller=seller, quantity=1, item=carrot)  # noqa

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
        print(validated_data)
        t = self.instance = Transaction.objects.create(buyer=buyer, seller=seller)  # noqa
        processed = False

        with transaction.atomic():
            t.status = 'completed'

            buy = validated_data.get('buy', [])

            sell = validated_data.get('sell', [])
            for item in sell:
                inventory = SellerInventory.objects.filter(  # noqa
                    seller=seller,
                    quantity__gte=item.get('quantity', 0),
                    item__name=item.get('name', '').capitalize(),
                )
                if inventory.exists():
                    [inventory] = inventory
                    price = inventory.item.price.seller
                    balance = buyer.balance
                    processed = True
                else:
                    processed = False

        t.status = 'completed' if processed else 'canceled'
        t.save()

        return self.instance
