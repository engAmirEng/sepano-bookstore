from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.shortcuts import get_object_or_404
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


class ItemRelatedField(serializers.RelatedField):
    queryset = Item.objects.sellable()

    def to_internal_value(self, data):
        return get_object_or_404(self.queryset, pk=data)


class CartSerializer(serializers.Serializer):
    pk = serializers.IntegerField(read_only=True)
    quantity = serializers.IntegerField(write_only=True, validators=[MinValueValidator(0)])
    item = ItemRelatedField(write_only=True)
    items = OrderItemSerializer(many=True, read_only=True, source="order_orderitems")
    total_price = serializers.DecimalField(read_only=True, max_digits=7, decimal_places=2)

    def create(self, validated_data):
        user = self.context["request"].user
        cart, err = Order.objects.add_to_cart(user=user, **validated_data)
        if err is not None:
            raise serializers.ValidationError(err)
        return cart
