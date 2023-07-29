import pytest
from rest_framework import status

from name_goes_here.book.models import Author
from name_goes_here.users.tests.factories import user_with_perm_fac

pytestmark = pytest.mark.django_db


class TestAuthorViewSet:
    def test_change(self, authors, api_client):
        an_author = authors[0]
        user = user_with_perm_fac(permissions=["change_author"], model=Author)()
        api_client.force_authenticate(user=user)

        r = api_client.put(f"/api/authors/{an_author.pk}/", data={"name": "hello"})

        assert r.status_code == status.HTTP_200_OK
        assert r.json()["name"] == "hello"
