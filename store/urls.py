from django.urls import path
from .views import (
    CategoryListCreateView,
    CategoryDetailView,
    ProductListCreateView,
    ProductDetailView,
    OrderCreateView,
    UserRegistrationView,
    UserDetailView, OrderDetailView
)

urlpatterns = [
     path("register/", UserRegistrationView.as_view(), name="user-register"),
    path("users/<int:pk>/", UserDetailView.as_view(), name="user-detail"),
    path("users/", UserRegistrationView.as_view(), name="user-detail"),
    path("categories/", CategoryListCreateView.as_view(), name="category-list-create"),
    path("categories/<int:pk>/", CategoryDetailView.as_view(), name="category-detail"),
    path("products/", ProductListCreateView.as_view(), name="product-list-create"),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="product-detail"),
    path("orders/", OrderCreateView.as_view(), name="order-create"),
    path("orders/<int:pk>/", OrderDetailView.as_view(), name="order-detail")
]
