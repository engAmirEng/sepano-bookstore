from django.contrib.auth import get_user_model
from rest_framework.mixins import (
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    CreateModelMixin,
    DestroyModelMixin,
)
from rest_framework.viewsets import GenericViewSet

from .serializers import AuthorSerializer, BookSerializer
from ..models import Author, Book

User = get_user_model()


class AuthorViewSet(
    ListModelMixin, CreateModelMixin, DestroyModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet
):
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()

class BookViewSet(
    ListModelMixin, CreateModelMixin, DestroyModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet
):
    serializer_class = BookSerializer
    queryset = Book.objects.all()
