from django.urls import reverse
from drf_extra_fields.fields import Base64ImageField
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from .models import Seller


class CreateSellerSerializer(serializers.ModelSerializer):
    link = serializers.SerializerMethodField()

    class Meta:
        model = Seller
        fields = ['id', 'link']
        read_only_fields = ['id', 'link']

    @extend_schema_field(serializers.CharField)
    def get_link(self, seller):  # noqa
        return reverse('game', kwargs={'seller': seller.id})


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
    quantity = serializers.IntegerField()


class CreateTransactionSerializer(serializers.Serializer):
    buyer = serializers.CharField(max_length=36)
    seller = serializers.CharField(max_length=36)
    buy = ItemSerializer(many=True)
    sell = ItemSerializer(many=True)
