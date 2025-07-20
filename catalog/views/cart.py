# catalog/views/cart.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from catalog.models import Cart, CartItem, Product

@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.items.select_related('product').all()
    total_cart_price = sum(item.total_price for item in items)
    return render(request, 'catalog/cart.html', {
        'cart': cart,
        'items': items,
        'total_cart_price': total_cart_price
    })

@login_required
def cart_add(request, product_id):
    cart, created = Cart.objects.get_or_create(user=request.user)
    product = Product.objects.get(pk=product_id)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    return redirect('product_list')

@login_required
def cart_remove(request, product_id):
    cart, created = Cart.objects.get_or_create(user=request.user)
    try:
        item = CartItem.objects.get(cart=cart, product_id=product_id)
        item.delete()
    except CartItem.DoesNotExist:
        pass
    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    return redirect('cart_detail')

@login_required
def cart_increase(request, product_id):
    cart, created = Cart.objects.get_or_create(user=request.user)
    try:
        item = CartItem.objects.get(cart=cart, product_id=product_id)
        item.quantity += 1
        item.save()
        return JsonResponse({'success': True, 'quantity': item.quantity, 'total_price': float(item.total_price)})
    except CartItem.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Товар не найден в корзине'})

@login_required
def cart_decrease(request, product_id):
    cart, created = Cart.objects.get_or_create(user=request.user)
    try:
        item = CartItem.objects.get(cart=cart, product_id=product_id)
        if item.quantity > 1:
            item.quantity -= 1
            item.save()
            return JsonResponse({'success': True, 'quantity': item.quantity, 'total_price': float(item.total_price)})
        else:
            item.delete()
            return JsonResponse({'success': True, 'quantity': 0, 'total_price': 0, 'removed': True})
    except CartItem.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Товар не найден в корзине'}) 