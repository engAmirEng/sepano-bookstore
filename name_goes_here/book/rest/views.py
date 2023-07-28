from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from rest_framework.viewsets import GenericViewSet

from ..filters import BookFilter
from ..models import Author, Book
from .serializers import AuthorSerializer, BookSerializer

User = get_user_model()


class AuthorViewSet(
    ListModelMixin, CreateModelMixin, DestroyModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet
):
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ("name", "user__name", "user__username")


class BookViewSet(
    ListModelMixin, CreateModelMixin, DestroyModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet
):
    serializer_class = BookSerializer
    queryset = Book.objects.all()
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly,)
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_class = BookFilter
    search_fields = ("title", "description")
    ordering_fields = ("price", "stock_quantity", "publication_date")
