from django.conf import settings
from django.urls import include, path
from rest_framework_nested import routers

from name_goes_here.book.rest.views import AuthorViewSet, BookViewSet
from name_goes_here.shopping.rest.views import OrderItemViewSet, OrderViewSet
from name_goes_here.users.rest.views import UserViewSet

if settings.DEBUG:
    router = routers.DefaultRouter()
else:
    router = routers.SimpleRouter()

# users app
router.register("users", UserViewSet)

# book app
router.register("authors", AuthorViewSet)
router.register("books", BookViewSet)

# shopping app
router.register("orders", OrderViewSet, basename="order")
orders_router = routers.NestedSimpleRouter(router, r"orders", lookup="orders")
orders_router.register(r"order-items", OrderItemViewSet, basename="order-orderitems")


app_name = "rest"
urlpatterns = [
    path("", include(router.urls)),
    path("", include(orders_router.urls)),
    path("", include("name_goes_here.shopping.rest.urls")),
    # Other paths (maybe ApiViews)
]
