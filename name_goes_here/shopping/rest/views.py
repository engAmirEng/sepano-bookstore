from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from name_goes_here.utils.permissions import DjangoFullModelPermissions

from ..models import Order
from .serializers import CartSerializer, OrderItemSerializer, OrderSerializer

User = get_user_model()


class OrderViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes = (DjangoFullModelPermissions,)

    def get_permissions(self):
        if self.action in ("mine_detail", "mine_list"):
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = self.permission_classes

        return [permission() for permission in permission_classes]

    @action(detail=False, url_path="mine")
    def mine_detail(self, request):
        serializer = self.serializer_class(self.queryset.for_user(self.request.user), many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @action(detail=True, url_path="mine")
    def mine_list(self, request, pk):
        serializer = self.serializer_class(get_object_or_404(self.queryset.for_user(self.request.user), pk=pk))
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class OrderItemViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    serializer_class = OrderItemSerializer
    permission_classes = (DjangoFullModelPermissions,)

    def get_permissions(self):
        if self.action in ("mine_detail", "mine_list"):
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = self.permission_classes

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        order = get_object_or_404(Order.objects.prefetch_related("order_orderitems"), pk=self.kwargs["orders_pk"])
        return order.order_orderitems.all()

    @action(detail=False, url_path="mine")
    def mine_detail(self, request, orders_pk):
        queryset = self.get_queryset()
        mine_order = get_object_or_404(Order.objects.for_user(self.request.user), pk=orders_pk)
        serializer = self.serializer_class(queryset.filter(order=mine_order), many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @action(detail=True, url_path="mine")
    def mine_list(self, request, orders_pk, pk):
        queryset = self.get_queryset()
        mine_order = get_object_or_404(Order.objects.for_user(self.request.user), pk=orders_pk)
        serializer = self.serializer_class(get_object_or_404(queryset.filter(order=mine_order), pk=pk))
        return Response(status=status.HTTP_200_OK, data=serializer.data)


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
