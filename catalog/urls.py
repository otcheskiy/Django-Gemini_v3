# catalog/urls.py
from django.urls import path, include
from rest_framework import routers
from . import views
from django.shortcuts import render
from .views import MyOrdersAPIView

router = routers.DefaultRouter()
router.register(r'products', views.ProductViewSet, basename='product')
router.register(r'categories', views.CategoryViewSet, basename='category')
router.register(r'images', views.ProductImageViewSet, basename='productimage')

urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('api/v1/products-list/', views.ProductListAPIView.as_view(), name='product_list_api'),
    path('api/v1/filters/', views.FiltersAPIView.as_view(), name='filters_api'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('cart/increase/<int:product_id>/', views.cart_increase, name='cart_increase'),
    path('cart/decrease/<int:product_id>/', views.cart_decrease, name='cart_decrease'),
    path('order/create/', views.create_order, name='create_order'),
    path('order/<int:order_id>/', lambda request, order_id: render(request, 'catalog/order_detail.html', {'order_id': order_id}), name='order_detail'),
    path('api/v1/my-orders/', MyOrdersAPIView.as_view(), name='my_orders_api'),
    path('products/<slug:product_slug>/', views.product_detail, name='product_detail'),
]