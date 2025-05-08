from core.utils.api_response import custom_reponse_validate_error, custom_response
from django.core.files.uploadedfile import InMemoryUploadedFile
from drf_spectacular.utils import extend_schema
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from datetime import datetime
from src.app.models.sales import Sales
from src.app.controllers.sales_controllers import handle_import_sales, get_revenue_by_date
from src.app.serializers.sales_serializer import (
    SalesSerializer,
    ImportSalesSerializer
)


class SalesViewSet(viewsets.ModelViewSet):
    queryset = Sales.objects.all()
    serializer_class = SalesSerializer
    permission_classes = (permissions.AllowAny,)

    # @extend_schema(
    #     request=ImportSalesSerializer,
    #     responses={201: 'Success'},
    # )
    @action(detail=False, methods=["POST"], url_path="import-sales")
    def import_sale(self, request, *args, **kwargs):
        sz = ImportSalesSerializer(data=request.data)
        if not sz.is_valid():
            return custom_reponse_validate_error(sz)

        file: InMemoryUploadedFile = sz.validated_data.get('file')
        success, msg_error, total_row = handle_import_sales(file)
        if not success:
            return custom_response(status_code=400, message=msg_error, data={})
        return custom_response(status_code=201, message="success", data={'imported_row': total_row})
