from rest_framework import status
from rest_framework.test import APITestCase
from .models import Receipt


data = {"user": "Will",
        "check_number": 12345,
        "shop": "REEBOK",
        "product": [{
               "name": "Chair",
               "count": 2,
               "price": 1800,
               "product_sum": 13245
        },
        {
                "name": "Glass",
                "count": 2,
                "price": 1550,
                "product_sum": 13245
        }],
        "date_of_issue": "2021-09-27 15:05:02",
        "total_sum": 12345
}


class ApiEndpointsTests(APITestCase):

    def test_sending_receipt(self):
        """
        Ensure we can post a new receipt.
        """
        response = self.client.post('/api/receipt', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Receipt.objects.count(), 1)
        self.assertEqual(Receipt.objects.get().user, 'Will')
        
        

