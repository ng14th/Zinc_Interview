from django.test import TestCase
from rest_framework.test import APIClient
from django.utils.timezone import make_aware
from datetime import datetime, timedelta
from src.app.models import Sales


class DailyRevenueMetricsTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        base_date = datetime.strptime("03/01/2026", "%m/%d/%Y")

        # Seed sales for 3 days: 03/01, 03/02, 03/03
        for i in range(3):
            date = make_aware(base_date + timedelta(days=i))
            for _ in range(i + 1):  # 1 sale on day 1, 2 on day 2, 3 on day 3
                Sales.objects.create(
                    sale_date=date,
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

    def test_daily_revenue_metrics(self):
        response = self.client.get("/api/metrics/revenue/daily/", {
            "start": "03/01/2026",
            "end": "03/03/2026"
        })

        self.assertEqual(response.status_code, 200)
        data = response.json()["data"]

        # Convert to dictionary for easier assertions
        revenue_by_date = {entry["date"]: entry["revenue_sgd"] for entry in data}

        self.assertEqual(revenue_by_date["2026-03-01"], 10.0)  # 1 sale
        self.assertEqual(revenue_by_date["2026-03-02"], 20.0)  # 2 sales
        self.assertEqual(revenue_by_date["2026-03-03"], 30.0)  # 3 sales
