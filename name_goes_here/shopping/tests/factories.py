import random
from decimal import Decimal

import factory
from factory import SubFactory, lazy_attribute
from factory.django import DjangoModelFactory

from name_goes_here.shopping.models import Order
from name_goes_here.users.tests.factories import UserFactory


class OrderFactory(DjangoModelFactory):
    user = SubFactory(UserFactory)
    status = factory.Iterator([choice[0] for choice in Order.Status.choices])

    class Meta:
        model = Order

    @lazy_attribute
    def total_price(self):
        # Generate a random decimal with 2 decimal places
        return Decimal("%.2f" % random.uniform(1, 1000))
