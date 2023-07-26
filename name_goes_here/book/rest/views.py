from django.contrib.auth import get_user_model
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.viewsets import GenericViewSet

from ..models import Author, Book
from .serializers import AuthorSerializer, BookSerializer

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
