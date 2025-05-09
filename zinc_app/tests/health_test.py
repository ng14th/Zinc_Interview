from django.test import TestCase
from rest_framework.test import APIClient
from django.utils.timezone import make_aware
from datetime import datetime
from src.app.models import Sales


class HealthTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_revenue_metrics(self):
        response = self.client.get("/health/")

        self.assertEqual(response.status_code, 200)
        data = response.json()

        # self.assertEqual(data["status"], "ok")
        # case fail
        self.assertEqual(data["status"], "not ok")
