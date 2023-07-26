from decimal import Decimal

from django.apps import apps
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.utils.translation import gettext_lazy as _


class OrderQuerySet(models.QuerySet):
    def for_user(self, user):
        return self.filter(user=user)

    def get_or_create_cart(self, user):
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


class OrderItem(models.Model):
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
