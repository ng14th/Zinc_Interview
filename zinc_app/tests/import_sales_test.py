import io
import csv
from rest_framework.test import APITestCase
from rest_framework import status
from src.app.models import Sales  # Adjust import as needed
from src.dj_project.settings import *


class ImportSalesTestCase(APITestCase):
    def setUp(self):

        self.valid_csv_headers = [
            'Sale Date', 'Client ID', 'Sale ID',
            'Item name', 'Batch #', 'Sales Notes',
            'Location', 'Notes', 'Color', 'Size',
            'Item price (excluding tax)', 'Quantity',
            'Subtotal (excluding tax)', 'Discount %',
            'Discount amount', 'Tax', 'Item Total',
            'Total Paid w/ Payment Method', 'Payment Method'
        ]

        self.valid_csv_row = [
            '3/1/2025', '100002649', '3971',
            '10 Practice Credits', '---', '',
            'Golf - experience', '', '---', '---',
            '32', '1',
            '32', '0',
            '0', '2.88', '34.88',
            '34.88', 'Credit card (AMEX-Keyed)'
        ]

    def create_csv_file(self, headers, row):
        file_stream = io.StringIO()
        writer = csv.writer(file_stream)
        writer.writerow(headers)
        writer.writerow(row)
        file_stream.seek(0)
        return io.BytesIO(file_stream.getvalue().encode('utf-8'))

    def test_valid_import_sales(self):
        csv_file = self.create_csv_file(
            self.valid_csv_headers,
            self.valid_csv_row
        )
        csv_file.name = 'sales.csv'

        response = self.client.post(
            path='/api/sales/import-sales/',
            data={'file': csv_file},
            format='multipart'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data_response = response.data['data']['imported_row']
        self.assertEqual(Sales.objects.count(), data_response)
