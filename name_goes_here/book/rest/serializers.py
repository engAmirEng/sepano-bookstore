from django.contrib.auth import get_user_model
from rest_framework import serializers

from ..models import Author, Book

User = get_user_model()


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["id", "name", "user"]


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["id", "title", "author", "price", "description", "publication_date", "stock_quantity"]
