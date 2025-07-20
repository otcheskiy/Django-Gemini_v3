# catalog/views/auth.py
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from catalog.models import Cart, CartItem, Product

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('product_list')
    else:
        form = UserCreationForm()
    return render(request, 'catalog/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            session_cart = request.session.get('cart')
            if session_cart:
                cart, _ = Cart.objects.get_or_create(user=user)
                for product_id, quantity in session_cart.items():
                    try:
                        product = Product.objects.get(pk=product_id)
                        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
                        if not created:
                            cart_item.quantity += int(quantity)
                        else:
                            cart_item.quantity = int(quantity)
                        cart_item.save()
                    except Product.DoesNotExist:
                        continue
                del request.session['cart']
                request.session.modified = True
            return redirect('product_list')
    else:
        form = AuthenticationForm()
    return render(request, 'catalog/login.html', {'form': form})

def logout_view(request):
    auth_logout(request)
    return redirect('product_list') 