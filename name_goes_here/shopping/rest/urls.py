from django.urls import path

from name_goes_here.shopping.rest.views import CardAPIView

urlpatterns = [
    path("cart/", CardAPIView.as_view()),
]
