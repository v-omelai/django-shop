import logging
import random

from django.core.exceptions import ValidationError
from django.db import transaction
from django.http import Http404
from django.views.generic import TemplateView
from rest_framework import status
from rest_framework.generics import UpdateAPIView, CreateAPIView
from rest_framework.response import Response

from apps.core.models import *
from apps.core.serializers import *


logger = logging.getLogger(__name__)


class LoadingPageView(TemplateView):
    template_name = 'pages/loading.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['text'] = random.choice([
            'Slicing onions...',
            'Chopping carrots...',
            'Boiling broccoli...',
            'Juicing oranges...',
            'Packing watermelons...',
        ])
        return context


class GamePageView(TemplateView):
    template_name = 'pages/game.html'

    @classmethod
    def scale(cls, entity=None):
        cells = ['&nbsp;'] * 12
        if entity:
            inventory = entity.inventory.all()
            items = list(inventory)
            cells = items + cells[len(items):]
        return cells

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            seller = Seller.objects.get(id=kwargs.get('seller'))  # noqa
            buyer = seller.buyer

            context.update({
                'seller': seller,
                'buyer': buyer,
                'inventory': {
                    'empty': self.scale(),
                    'seller': self.scale(seller),
                    'buyer': self.scale(buyer),
                }
            })
        except (ValidationError, Seller.DoesNotExist):  # noqa
            raise Http404('Not found')
        return context


class CreateSellerView(CreateAPIView):
    queryset = Seller.objects.all()  # noqa
    serializer_class = CreateSellerSerializer

    def perform_create(self, serializer):
        with transaction.atomic():
            # Initiate a buyer
            buyer = Buyer.objects.create(name='Vitalii Omelai', balance=500)  # noqa

            # Initiate a seller
            goal = Goal.objects.get(difficulty=1)  # noqa
            seller = Seller.objects.create(name='Player', balance=0, buyer=buyer, goal=goal)  # noqa

            # Add an apple
            apple = Item.objects.get(name='Apple')  # noqa
            SellerInventory.objects.create(seller=seller, quantity=1, item=apple)  # noqa

            # Add a carrot
            carrot = Item.objects.get(name='Carrot')  # noqa
            SellerInventory.objects.create(seller=seller, quantity=1, item=carrot)  # noqa

            return seller

    def create(self, request, *args, **kwargs):
        data = self.perform_create(None)
        serialized = self.get_serializer(data)
        return Response(serialized.data, status=status.HTTP_201_CREATED)


class UpdateSellerView(UpdateAPIView):
    queryset = Seller.objects.all()  # noqa
    serializer_class = UpdateSellerSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'seller'


class CreateTransactionView(CreateAPIView):
    queryset = Transaction.objects.all()  # noqa
    serializer_class = CreateTransactionSerializer

    def perform_create(self, serializer):
        data = serializer.validated_data
        buyer = Buyer.objects.get(id=data.get('buyer'))  # noqa
        seller = Seller.objects.get(id=data.get('seller'))  # noqa
        t = Transaction.objects.create(buyer=buyer, seller=seller)  # noqa
