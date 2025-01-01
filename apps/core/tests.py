from django.urls import reverse
from django.test import TestCase

from apps.core.models import Seller
from populate import populate, DIFFICULTIES


class SellerTransactionTest(TestCase):
    def setUp(self):  # noqa
        populate()

    def test_seller_transaction_flow(self):
        response = self.client.post(reverse('api-create-seller'), content_type='application/json')
        self.assertEqual(response.status_code, 201)

        seller = Seller.objects.get(id=response.json()['id'])  # noqa
        buyer = seller.buyer

        data = {
            'buyer': buyer.id,
            'seller': seller.id,
            'items': {},
        }

        response = self.client.post(reverse('api-create-transaction'), data, content_type='application/json')
        self.assertEqual(response.status_code, 422)

        for dictionary in DIFFICULTIES:
            data['items'] = dictionary['items']
            response = self.client.post(reverse('api-create-transaction'), data, content_type='application/json')
            self.assertEqual(response.status_code, 201)

        self.assertIsNotNone(response.json()['link'])
