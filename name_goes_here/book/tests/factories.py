from factory import Faker
from factory.django import DjangoModelFactory

from name_goes_here.book.models import Author


class AuthorFactory(DjangoModelFactory):
    name = Faker("name")

    class Meta:
        model = Author
