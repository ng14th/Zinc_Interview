from datetime import datetime
from core.utils.api_response import custom_response
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from src.app.models.sales import SummarySalesByDate
from src.app.controllers.sales_controllers import get_revenue_daily_v2, get_revenue_by_date_v2
from src.app.serializers.sales_serializer import SalesSerializer

class SalesMetricsViewSetV2(viewsets.ModelViewSet):
    queryset = SummarySalesByDate.objects.all()
    serializer_class = SalesSerializer
    permission_classes = (permissions.AllowAny,)

    @action(detail=False, methods=["GET"], url_path="revenue")
    def revenue_sale_v2(self, request, *args, **kwargs):

        start = request.GET.get('start')
        end = request.GET.get('end')

        if not any([start, end]):
            return custom_response(status_code=400, message="Missing start or end", data={})

        try:
            start = datetime.strptime(start, '%m/%d/%Y')
            end = datetime.strptime(end, '%m/%d/%Y')
        except ValueError:
            return custom_response(status_code=400, message="Invalid date format", data={})

        data = get_revenue_by_date_v2(start, end)

        return custom_response(status_code=200, message="success", data=data)

    @action(detail=False, methods=["GET"], url_path="revenue/daily")
    def revenue_daily_v2(self, request, *args, **kwargs):

        start = request.GET.get('start')
        end = request.GET.get('end')

        if not any([start, end]):
            return custom_response(status_code=400, message="Missing start or end", data={})

        try:
            start = datetime.strptime(start, '%m/%d/%Y')
            end = datetime.strptime(end, '%m/%d/%Y')
        except ValueError:
            return custom_response(status_code=400, message="Invalid date format", data={})

        data = get_revenue_daily_v2(start, end)

        return custom_response(status_code=200, message="success", data=data)
