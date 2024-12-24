import logging
import random

from django.core.exceptions import ValidationError
from django.db import transaction
from django.http import Http404
from django.urls import reverse
from django.views.generic import TemplateView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core.models import *
from apps.core.serializers import *


logger = logging.getLogger(__name__)


class HomePageView(TemplateView):
    template_name = 'pages/home.html'

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            seller = Seller.objects.get(id=kwargs.get('seller'))  # noqa
            buyer = seller.buyer
        except (ValidationError, Seller.DoesNotExist):  # noqa
            raise Http404('Not found')
        context['seller'] = seller
        context['buyer'] = buyer
        return context


class GameAPIView(APIView):
    def post(self, request):
        try:
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
        except Exception as e:
            logger.error(e)
            return Response({'created': False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({
            'created': True,
            'redirect': reverse('game', kwargs={'seller': seller.id})
        }, status=status.HTTP_201_CREATED)
