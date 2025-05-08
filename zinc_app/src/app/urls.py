from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter
from .views import SalesViewSet, SalesMetricsViewSet

router = SimpleRouter()

router.register("sales", SalesViewSet)
router.register("metrics", SalesMetricsViewSet, basename="metrics")

urlpatterns = router.urls
