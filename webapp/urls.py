from django.urls import path
from .views import (
    OrderCreateAPI,
    StoreOrderListAPI,
    InventoryAPI,
    SmartSearch,
    Autocomplete
)

urlpatterns = [

    path("orders/", OrderCreateAPI.as_view()),

    path("stores/<int:store_id>/orders/", StoreOrderListAPI.as_view()),

    path("stores/<int:store_id>/inventory/", InventoryAPI.as_view()),

    path("search/products/", SmartSearch.as_view()),

    path("search/suggest/", Autocomplete.as_view()),
]
