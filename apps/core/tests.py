from django.urls import reverse
from django.test import TestCase

from apps.core.models import Seller
from populate import populate, ROOKIE, PROFESSIONAL, EXPERIENCED


class CoreTest(TestCase):
    def setUp(self):  # noqa
        populate()

    def test_workflow(self):
        response = self.client.post(reverse('api-create-seller'), content_type='application/json')

        self.assertEqual(response.status_code, 201)

        seller = Seller.objects.get(id=response.json()['id'])  # noqa
        buyer = seller.buyer

        for dictionary in [ROOKIE, EXPERIENCED, PROFESSIONAL]:
            data = {
                'buyer': buyer.id,
                'seller': seller.id,
                'items': dictionary['items'],
            }

            response = self.client.post(reverse('api-create-transaction'), data, content_type='application/json')

            self.assertEqual(response.status_code, 201)

            print(response.json())
