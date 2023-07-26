from django.contrib.auth import get_user_model
from rest_framework import serializers

from ..models import Order, OrderItem, get_item_model

User = get_user_model()
Item = get_item_model()


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["id", "total_price", "status", "order_date"]


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["id", "quantity", "fee_price"]
