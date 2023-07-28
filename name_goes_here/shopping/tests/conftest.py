import pytest

from .factories import OrderFactory


@pytest.fixture
def orders():
    return OrderFactory.create_batch(3)
