# catalog/views.py
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse

from rest_framework import viewsets, status # Добавил status для HTTP-кодов
from rest_framework.response import Response # Добавил Response для кастомных ответов
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Product, Category, ProductImage, Cart, CartItem, Order, OrderItem
from .serializers import ProductSerializer, CategorySerializer, ProductImageSerializer
from rest_framework.generics import ListAPIView
from django.db.models import Q
from rest_framework import generics

# Импорты для обработки изображений, если они будут загружаться по URL
# (Эти импорты нужны, если вы решите реализовать логику загрузки по URL в ViewSet,
# или если она уже в сериализаторе и вы хотите убедиться, что все импорты на месте)
# from django.core.files.base import ContentFile
# import requests
# import os
# import uuid

def product_list(request):
    from .models import Product
    product_list = Product.objects.all()
    paginator = Paginator(product_list, 6)  # товаров на странице
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # Фильтры
    categories = Category.objects.all()
    brand_choices = Product.BRAND_CHOICES
    material_choices = Product.MATERIAL_CHOICES
    gender_choices = Product.GENDER_CHOICES
    age_choices = Product.AGE_CHOICES
    color_choices = Product.COLOR_CHOICES
    return render(request, 'catalog/product_list.html', {
        'page_obj': page_obj,
        'categories': categories,
        'brand_choices': brand_choices,
        'material_choices': material_choices,
        'gender_choices': gender_choices,
        'age_choices': age_choices,
        'color_choices': color_choices,
    })

def product_detail(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    return render(request, 'catalog/product_detail.html', {'product': product})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('product_list')  # или на главную страницу
    else:
        form = UserCreationForm()
    return render(request, 'catalog/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            # --- Перенос корзины из сессии в модель Cart ---
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
            # --- конец переноса корзины ---
            return redirect('product_list')  # или на главную страницу
    else:
        form = AuthenticationForm()
    return render(request, 'catalog/login.html', {'form': form})

def logout_view(request):
    auth_logout(request)
    return redirect('product_list')

@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.items.select_related('product').all()
    
    # Вычисляем общую сумму корзины
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
    # Возврат на предыдущую страницу
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
def create_order(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.items.select_related('product').all()
    if not items:
        return redirect('cart_detail')  # Корзина пуста, не создаём заказ

    order = Order.objects.create(user=request.user)
    for item in items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price
        )
    # Очищаем корзину
    cart.items.all().delete()
    return redirect('order_detail', order_id=order.id)

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

class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # Удалена вся логика загрузки/обновления фото, теперь только ID

    def create(self, request, *args, **kwargs):
        external_id = request.data.get('external_id')
        if external_id:
            try:
                instance = Product.objects.get(external_id=external_id)
                serializer = self.get_serializer(instance, data=request.data, partial=True)
                serializer.is_valid(raise_exception=True)
                self.perform_update(serializer)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Product.DoesNotExist:
                pass  # Перейдём к созданию нового товара

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

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

class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        params = self.request.query_params

        categories = params.getlist('category')
        if categories:
            queryset = queryset.filter(category__name__in=categories)

        brands = params.getlist('brand')
        if brands:
            queryset = queryset.filter(brand__in=brands)

        materials = params.getlist('material')
        if materials:
            queryset = queryset.filter(material__in=materials)

        genders = params.getlist('gender')
        if genders:
            queryset = queryset.filter(gender__in=genders)

        ages = params.getlist('age')
        if ages:
            queryset = queryset.filter(age__in=ages)

        colors = params.getlist('color')
        if colors:
            queryset = queryset.filter(color__in=colors)

        temple_size_min = params.get('temple_size_min')
        if temple_size_min:
            queryset = queryset.filter(temple_size__gte=temple_size_min)
        temple_size_max = params.get('temple_size_max')
        if temple_size_max:
            queryset = queryset.filter(temple_size__lte=temple_size_max)

        lens_width_min = params.get('lens_width_min')
        if lens_width_min:
            queryset = queryset.filter(lens_width__gte=lens_width_min)
        lens_width_max = params.get('lens_width_max')
        if lens_width_max:
            queryset = queryset.filter(lens_width__lte=lens_width_max)

        bridge_width_min = params.get('bridge_width_min')
        if bridge_width_min:
            queryset = queryset.filter(bridge_width__gte=bridge_width_min)
        bridge_width_max = params.get('bridge_width_max')
        if bridge_width_max:
            queryset = queryset.filter(bridge_width__lte=bridge_width_max)

        return queryset

class FiltersAPIView(APIView):
    def get(self, request):
        category = request.query_params.get('category')
        qs = Product.objects.all()
        if category:
            qs = qs.filter(category__name=category)
        data = {
            'brand': qs.values_list('brand', flat=True).distinct(),
            'material': qs.values_list('material', flat=True).distinct(),
            'gender': qs.values_list('gender', flat=True).distinct(),
            'age': qs.values_list('age', flat=True).distinct(),
            'color': qs.values_list('color', flat=True).distinct(),
            'temple_size': qs.values_list('temple_size', flat=True).distinct(),
            'lens_width': qs.values_list('lens_width', flat=True).distinct(),
            'bridge_width': qs.values_list('bridge_width', flat=True).distinct(),
        }
        # Сначала убираем None и '', потом сортируем
        for k, v in data.items():
            filtered = [x for x in v if x not in [None, '']]
            data[k] = sorted(filtered)
        return Response(data)