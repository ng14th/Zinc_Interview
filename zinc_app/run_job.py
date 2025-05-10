#!/usr/bin/env python
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.dj_project.settings')
django.setup()


def summary_sales_by_date():
    from src.app.models import Sales, SummarySalesByDate
    from django.db.models import Sum, Count

    sales = Sales.objects.filter()
    summary_sales_by_date = sales\
        .values('sale_date')\
        .annotate(
            total_orders=Count('id'),
            total_revenue=Sum('total_paid')
        )
    SummarySalesByDate.objects.all().delete()

    bulk_objects = [
        SummarySalesByDate(
            sale_date=sale['sale_date'],
            total_orders=sale['total_orders'],
            total_revenue=sale['total_revenue'],
        ) for sale in summary_sales_by_date
    ]

    SummarySalesByDate.objects.bulk_create(bulk_objects)


if __name__ == "__main__":
    summary_sales_by_date()
