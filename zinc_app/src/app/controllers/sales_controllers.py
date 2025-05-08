import csv
import io
from datetime import datetime
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models import Sum, Count, F
from src.app.models.sales import Sales


VALID_HEADER = [
    'Sale Date', 'Client ID', 'Sale ID',
    'Item name', 'Batch #', 'Sales Notes',
    'Location', 'Notes', 'Color', 'Size',
    'Item price (excluding tax)', 'Quantity',
    'Subtotal (excluding tax)', 'Discount %',
    'Discount amount', 'Tax', 'Item Total',
    'Total Paid w/ Payment Method', 'Payment Method'
]


def get_data_from_csv(request_file: InMemoryUploadedFile):
    success = True
    msg_error = ''
    total_row = 0
    # Move the pointer to the beginning in case it's been read before
    request_file.seek(0)
    # Wrap the byte stream into a text stream
    text_stream = io.TextIOWrapper(
        request_file.file,
        encoding='utf-8',
        newline=''
    )

    reader = csv.reader(text_stream)
    headers = next(reader, [])  # Read the first row

    # check if headers are valid
    if sorted(headers) != sorted(VALID_HEADER):
        success = False
        msg_error = 'Invalid file headers'
        return success, msg_error, total_row

    values_by_row = []
    # spearator data csv
    for row in reader:
        row_dict = {header: value for header, value in zip(headers, row)}
        values_by_row.append(row_dict)

    list_objects = [
        Sales(
            sale_date=datetime.strptime(
                row.get('Sale Date'),
                '%m/%d/%Y'
            ).date(),
            client_id=row.get('Client ID'),
            sale_id=row.get('Sale ID'),
            item_name=row.get('Item name'),
            batch=row.get('Batch #') if row.get('Batch #') != '---' else None,
            sale_notes=row.get('Sales Notes'),
            location=row.get('Location'),
            notes=row.get('Notes'),
            color=row.get('Color') if row.get('Color') != '---' else None,
            size=row.get('Size') if row.get('Size') != '---' else None,
            item_price=row.get('Item price (excluding tax)'),
            quantity=row.get('Quantity'),
            subtotal=row.get('Subtotal (excluding tax)'),
            discount=row.get('Discount %'),
            tax=row.get('Tax'),
            item_total=row.get('Item Total'),
            total_paid=row.get('Total Paid w/ Payment Method'),
            payment_method=row.get('Payment Method'),
        ) for row in values_by_row
    ]

    Sales.objects.bulk_create(list_objects)
    total_row = Sales.objects.count()

    return success, msg_error, total_row


def handle_import_sales(file: InMemoryUploadedFile):
    success = True
    msg_error = ''
    total_row = 0

    if file.content_type != 'text/csv':
        success = False
        msg_error = 'Invalid file type - must be CSV'

    success, msg_error, total_row = get_data_from_csv(file)

    return success, msg_error, total_row


def get_revenue_by_date(start, end):
    data = Sales.objects\
        .filter(sale_date__range=[start, end])\
        .aggregate(
            total_revenue_sgd=Sum('total_paid'),
            average_order_value_sg=Sum('total_paid') / Count('id') if Count('id') else 0)

    data['average_order_value_sg'] = round(data['average_order_value_sg'], 2)
    return data


def get_revenue_daily(start, end):
    data = Sales.objects\
        .filter(sale_date__range=[start, end])\
        .order_by('sale_date')\
        .values(date=F('sale_date'))\
        .annotate(
            revenue_sgd=Sum('total_paid')
        )

    return data
