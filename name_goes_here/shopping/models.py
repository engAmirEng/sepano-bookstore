from decimal import Decimal
from typing import Protocol

from django.apps import apps
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db import models, transaction
from django.utils.translation import gettext_lazy as _


class OrderQuerySet(models.QuerySet):
    def for_user(self, user):
        return self.filter(user=user)

    @transaction.atomic
    def add_to_cart(self, user, item, quantity: int):
        """
        Adds an item to the Cart(an Order with status of open)
        """
        cart, is_created = self.get_or_create_cart(user=user)
        try:
            existing_ot = OrderItem.objects.filter(order=cart, item=item).get()
        except OrderItem.DoesNotExist:
            pass
        else:
            existing_ot.delete()
        OrderItem.objects.create_based_on_item(item=item, cart=cart, quantity=quantity)
        cart.refresh_from_db()
        cart.recalculate_total_price()
        return cart

    def get_or_create_cart(self, user) -> "Order":
        return self.get_or_create(status=Order.Status.OPEN, user=user, defaults={"total_price": Decimal(0)})


class Order(models.Model):
    """
    Represents order and cart at the same time
    """

    objects = OrderQuerySet.as_manager()

    class Status(models.TextChoices):
        OPEN = "OP", _("open")
        PENDING = "PE", _("pending")
        DONE = "DO", _("done")

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="user_orders")
    total_price = models.DecimalField(max_digits=7, decimal_places=2)
    status = models.CharField(max_length=4, choices=Status.choices)
    order_date = models.DateField(auto_now_add=True)

    def recalculate_total_price(self):
        """
        call this after any orderitem changed
        """
        assert self.status == Order.Status.OPEN
        total_price = 0
        for i in self.order_orderitems.all():
            total_price += i.total_price
        self.total_price = total_price
        self.save()


class ItemProto(Protocol):
    price: int


class OrderItemQueryset(models.QuerySet):
    def create_based_on_item(self, item: ItemProto, quantity: int, cart: Order) -> "OrderItem":
        """
        Creates an item to be added to the cart
        """
        od = OrderItem()
        od.order = cart
        od.quantity = quantity
        od.item = item
        od.fee_price = item.price
        od.save()
        return od


class OrderItem(models.Model):
    objects = OrderItemQueryset.as_manager()

    order = models.ForeignKey("Order", on_delete=models.CASCADE, related_name="order_orderitems")
    item = models.ForeignKey(settings.ITEM_MODEL, on_delete=models.PROTECT, related_name="item_orderitems")
    quantity = models.PositiveIntegerField()
    fee_price = models.DecimalField(max_digits=6, decimal_places=2)

    @property
    def total_price(self) -> Decimal:
        return self.quantity * self.fee_price


def get_item_model() -> models.Model:
    """
    Return the User model that is active in this project.
    """
    try:
        return apps.get_model(settings.ITEM_MODEL, require_ready=False)
    except ValueError:
        raise ImproperlyConfigured("ITEM_MODEL must be of the form 'app_label.model_name'")
    except LookupError:
        raise ImproperlyConfigured("ITEM_MODEL refers to model '%s' that has not been installed" % settings.ITEM_MODEL)
