from django.conf import settings
from django.db import models
from django.db.models import CheckConstraint, Q
from django.utils.translation import gettext_lazy as _

from name_goes_here.shopping.models import AbstractItem, ItemQuerySet


class BookQuerySet(ItemQuerySet):
    def sellable(self):
        """
        Available books to sell
        """
        return self.all()


class Book(AbstractItem):
    objects = BookQuerySet.as_manager()

    title = models.CharField(max_length=255)
    author = models.ForeignKey("Author", on_delete=models.PROTECT, related_name="author_books")
    description = models.TextField(blank=True, null=True)
    publication_date = models.DateField()


class Author(models.Model):
    name = models.CharField(max_length=127, null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        constraints = [
            CheckConstraint(
                check=Q(name__isnull=False) | Q(user__isnull=False),
                name="provide_at_least_name_or_user",
                violation_error_message=_("provide either of name or user at least"),
            )
        ]
