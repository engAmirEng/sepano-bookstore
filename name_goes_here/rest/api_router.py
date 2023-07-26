from django.conf import settings
from django.urls import include, path
from rest_framework.routers import DefaultRouter, SimpleRouter

from name_goes_here.book.rest.views import AuthorViewSet, BookViewSet
from name_goes_here.users.rest.views import UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

# users app
router.register("users", UserViewSet)

# book app
router.register("author", AuthorViewSet)
router.register("book", BookViewSet)


app_name = "rest"
urlpatterns = [
    path("", include(router.urls)),
    # Other paths (maybe ApiViews)
]
