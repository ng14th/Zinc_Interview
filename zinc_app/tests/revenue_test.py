from django.test import TestCase
from rest_framework.test import APIClient
from django.utils.timezone import make_aware
from datetime import datetime
from src.app.models import Sales


class RevenueMetricsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create 5 sales with known total_paid values
        sale_date = make_aware(datetime.strptime("03/01/2026", "%m/%d/%Y"))
        for i in range(5):
            Sales.objects.create(
                sale_date=sale_date,
                client_id=1,
                sale_id=1,
                item_name="Item A",
                item_price=10.0,
                quantity=1,
                subtotal=10.0,
                discount=0,
                tax=0,
                item_total=10.0,
                total_paid=10.0,
                payment_method="Cash"
            )

    def test_revenue_metrics(self):
        response = self.client.get(
            "/api/metrics/revenue/",
            {
                "start": "03/01/2026",
                "end": "03/01/2026"
            }
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()["data"]

        self.assertEqual(data["total_revenue_sgd"], 50.0)
        self.assertEqual(data["average_order_value_sg"], 10.0)
