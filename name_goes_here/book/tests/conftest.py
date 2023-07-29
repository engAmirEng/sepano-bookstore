import pytest

from name_goes_here.book.tests.factories import AuthorFactory


@pytest.fixture
def authors():
    return AuthorFactory.create_batch(3)
