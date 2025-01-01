import logging
import random

from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView
from rest_framework.generics import UpdateAPIView, CreateAPIView

from apps.core.models import Seller, Transaction
from apps.core.serializers import CreateSellerSerializer, UpdateSellerSerializer, CreateTransactionSerializer

logger = logging.getLogger(__name__)


class LoadingPageView(TemplateView):
    template_name = 'pages/loading.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'text': random.choice([
                'Slicing onions...',
                'Chopping carrots...',
                'Boiling broccoli...',
                'Juicing oranges...',
                'Packing watermelons...',
            ])
        })
        return context


class CongratulationsPageView(TemplateView):
    template_name = 'pages/congratulations.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'text': random.choice([
                '🥳 Congratulations!',
                '🏆 You\'ve nailed it!',
                '🎮 The game is over!',
            ])
        })
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

    def dispatch(self, request, *args, **kwargs):
        self.seller = seller = get_object_or_404(Seller, id=kwargs.get('seller'))  # noqa
        if seller.goal is None:
            return redirect('congratulations')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        seller = self.seller
        buyer = self.seller.buyer
        context.update({
            'seller': seller,
            'buyer': buyer,
            'inventory': {
                'empty': self.scale(),
                'seller': self.scale(seller),
                'buyer': self.scale(buyer),
            }
        })
        return context


class CreateSellerView(CreateAPIView):
    queryset = Seller.objects.all()  # noqa
    serializer_class = CreateSellerSerializer


class UpdateSellerView(UpdateAPIView):
    queryset = Seller.objects.all()  # noqa
    serializer_class = UpdateSellerSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'seller'


class CreateTransactionView(CreateAPIView):
    queryset = Transaction.objects.all()  # noqa
    serializer_class = CreateTransactionSerializer
