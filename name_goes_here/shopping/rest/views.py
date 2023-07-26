from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet

from ..models import Order, OrderItem
from .serializers import OrderItemSerializer, OrderSerializer

User = get_user_model()


class OrderViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    serializer_class = OrderSerializer

    def get_queryset(self) -> QuerySet:
        return Order.objects.for_user(self.request.user)


class OrderItemViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    serializer_class = OrderItemSerializer

    def get_queryset(self):
        return OrderItem.objects.filter(order_id=self.kwargs["orders_pk"])
