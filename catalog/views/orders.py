# catalog/views/orders.py
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from catalog.models import Cart, CartItem, Order, OrderItem, Product

@login_required
def create_order(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.items.select_related('product').all()
    if not items:
        return redirect('cart_detail')
    order = Order.objects.create(user=request.user)
    for item in items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price
        )
    cart.items.all().delete()
    return redirect('order_detail', order_id=order.id)

class MyOrdersAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user).order_by('-created_at').prefetch_related('items__product')
        data = []
        for order in orders:
            items = []
            for item in order.items.all():
                items.append({
                    'product_id': item.product.id,
                    'product_name': item.product.name,
                    'quantity': item.quantity,
                    'price': float(item.price),
                })
            data.append({
                'id': order.id,
                'created_at': order.created_at,
                'status': order.status,
                'items': items,
            })
        return Response(data) 