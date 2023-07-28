import pytest
from rest_framework import status

from name_goes_here.shopping.models import Order
from name_goes_here.shopping.tests.factories import OrderFactory
from name_goes_here.users.tests.factories import uer_with_perm_fac

pytestmark = pytest.mark.django_db


class TestOrderViewSet:
    def test_read_403_if_no_perm(self, orders, api_client):
        api_client.force_authenticate(user={})

        r = api_client.get("/api/orders/")

        assert r.status_code == status.HTTP_403_FORBIDDEN

        r = api_client.get(f"/api/orders/{orders[0].pk}/")

        assert r.status_code == status.HTTP_403_FORBIDDEN

    def test_read(self, orders, api_client):
        user = uer_with_perm_fac(permissions=["view_order"], model=Order)()
        api_client.force_authenticate(user=user)

        r = api_client.get("/api/orders/")

        assert r.status_code == status.HTTP_200_OK
        assert [i["id"] for i in r.json()["results"]] == [i.pk for i in orders]

        r = api_client.get(f"/api/orders/{orders[0].pk}/")

        assert r.status_code == status.HTTP_200_OK
        assert r.json()["id"] == orders[0].pk

    def test_mine(self, user, api_client):
        orders = OrderFactory.create_batch(5, user=user)
        api_client.force_authenticate(user=user)

        r = api_client.get("/api/orders/mine/")

        assert r.status_code == status.HTTP_200_OK
        assert [i["id"] for i in r.json()] == [i.pk for i in orders]
