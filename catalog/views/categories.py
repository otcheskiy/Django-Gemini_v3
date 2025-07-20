# catalog/views/categories.py
from rest_framework import viewsets
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from catalog.models import Category, Product
from catalog.serializers import CategorySerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

def product_list(request):
    product_list = Product.objects.all()
    paginator = Paginator(product_list, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
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