from rest_framework import serializers
from src.app.models.sales import Sales
from django.core.files.uploadedfile import InMemoryUploadedFile


class ImportSalesSerializer(serializers.Serializer):
    file = serializers.FileField()


class SalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sales
        fields = '__all__'
