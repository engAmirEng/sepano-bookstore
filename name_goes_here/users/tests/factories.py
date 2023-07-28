from collections.abc import Iterable, Sequence
from typing import Any

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db import models
from factory import Faker, post_generation
from factory.django import DjangoModelFactory


class UserFactory(DjangoModelFactory):
    username = Faker("user_name")
    email = Faker("email")
    name = Faker("name")

    @post_generation
    def password(self, create: bool, extracted: Sequence[Any], **kwargs):
        password = (
            extracted
            if extracted
            else Faker(
                "password",
                length=42,
                special_chars=True,
                digits=True,
                upper_case=True,
                lower_case=True,
            ).evaluate(None, None, extra={"locale": None})
        )
        self.set_password(password)

    class Meta:
        model = get_user_model()
        django_get_or_create = ["username"]


def user_with_perm_fac(permissions: Iterable["str"], model: type[models.Model]):
    class UserWithPermissionFactory(UserFactory):
        @post_generation
        def user_permissions(self, create, extracted, **kwargs):
            if not create:
                return

            # Add the desired permissions to the user
            content_type = ContentType.objects.get_for_model(model)
            perms = []
            for perm in permissions:
                perms.append(Permission.objects.get(content_type=content_type, codename=perm))
            self.user_permissions.add(*perms)

    return UserWithPermissionFactory
