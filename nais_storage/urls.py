from django.urls import path
from nais_storage.views import get_order_details

app_name = "nais_storage"

urlpatterns = [
    path('', get_order_details)
]