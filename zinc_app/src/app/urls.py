from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter
from .views import SalesViewSet, SalesMetricsViewSet, SalesMetricsViewSetV2

router = SimpleRouter()

router.register("sales", SalesViewSet)
router.register("metrics", SalesMetricsViewSet, basename="metrics")
router.register("v2/metrics", SalesMetricsViewSetV2, basename="metrics-v2")

urlpatterns = router.urls
