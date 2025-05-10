from django.db import models


class Sales(models.Model):
    sale_date = models.DateField()
    client_id = models.BigIntegerField()
    sale_id = models.BigIntegerField()
    item_name = models.TextField()
    batch = models.TextField(null=True, blank=True)
    sale_notes = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=255)
    notes = models.TextField(null=True, blank=True)
    color = models.CharField(max_length=255, null=True, blank=True)
    size = models.IntegerField(null=True, blank=True)
    item_price = models.DecimalField(
        max_digits=100,
        decimal_places=5,
        default=0
    )
    quantity = models.IntegerField()
    subtotal = models.DecimalField(
        max_digits=100,
        decimal_places=5,
        default=0
    )
    discount = models.DecimalField(
        max_digits=100,
        decimal_places=5,
        default=0
    )
    tax = models.DecimalField(
        max_digits=100,
        decimal_places=5,
        default=0
    )
    item_total = models.DecimalField(
        max_digits=100,
        decimal_places=5,
        default=0
    )
    total_paid = models.DecimalField(
        max_digits=100,
        decimal_places=5,
        default=0
    )
    payment_method = models.CharField(max_length=255)

    class Meta:
        indexes = [
            models.Index(fields=['sale_date'])
        ]


class SummarySalesByDate(models.Model):
    sale_date = models.DateField()
    total_orders = models.IntegerField()
    total_revenue = models.DecimalField(
        max_digits=100,
        decimal_places=5,
        default=0
    )

    class Meta:
        indexes = [
            models.Index(fields=['sale_date'])
        ]
