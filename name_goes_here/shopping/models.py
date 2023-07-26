import decimal

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Order(models.Model):
    class Status(models.TextChoices):
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
    def total_proce(self) -> decimal.Decimal:
        return self.quantity * self.fee_price
