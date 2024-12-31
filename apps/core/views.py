import logging
import random

from django.core.exceptions import ValidationError
from django.http import Http404
from django.views.generic import TemplateView
from rest_framework.generics import UpdateAPIView, CreateAPIView

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
            seller = Seller.objects.get(id=kwargs.get('seller', ''))  # noqa
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


class UpdateSellerView(UpdateAPIView):
    queryset = Seller.objects.all()  # noqa
    serializer_class = UpdateSellerSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'seller'


class CreateTransactionView(CreateAPIView):
    queryset = Transaction.objects.all()  # noqa
    serializer_class = CreateTransactionSerializer
