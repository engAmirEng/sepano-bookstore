from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from ..models import Order
from .serializers import CartSerializer, OrderItemSerializer, OrderSerializer

User = get_user_model()


class OrderViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    serializer_class = OrderSerializer

    def get_queryset(self) -> QuerySet:
        return Order.objects.for_user(self.request.user)


class OrderItemViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    serializer_class = OrderItemSerializer

    def get_queryset(self):
        order = get_object_or_404(
            Order.objects.for_user(self.request.user).prefetch_related("order_orderitems"), pk=self.kwargs["orders_pk"]
        )
        return order.order_orderitems.all()


class CardAPIView(APIView):
    def post(self, request):
        serializer = CartSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request):
        cart, is_created = Order.objects.get_or_create_cart(request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)
