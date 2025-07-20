# catalog/models.py
from django.db import models
from django.utils.text import slugify
from django.conf import settings
#from django.core.exceptions import ValidationError

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    image = models.ImageField(upload_to='products/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.image.name.split('/')[-1] if self.image else "No Image"

class Product(models.Model):
    BRAND_CHOICES = [
        ("Luceat", "Luceat"),
        ("Cormens", "Cormens"),
        ("MonSolis", "MonSolis"),
        ("Piccolo Pesce", "Piccolo Pesce"),
    ]
    MATERIAL_CHOICES = [
        ("металл", "металл"),
        ("пластик", "пластик"),
        ("комбинированные", "комбинированные"),
        ("титан", "титан"),
    ]
    GENDER_CHOICES = [
        ("мужские", "мужские"),
        ("женские", "женские"),
        ("унисекс", "унисекс"),
    ]
    AGE_CHOICES = [
        ("детские", "детские"),
        ("подростковые", "подростковые"),
    ]
    COLOR_CHOICES = [
        ("черный", "черный"),
        ("серебро", "серебро"),
        ("золото", "золото"),
        ("цветные", "цветные"),
    ]

    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    external_id = models.CharField(max_length=50, blank=True, null=True, unique=True)
    image = models.ForeignKey(ProductImage, null=True, blank=True, on_delete=models.SET_NULL)
    # categories = models.ManyToManyField(Category)
    slug = models.SlugField(unique=True, max_length=255)

    brand = models.CharField(max_length=32, choices=BRAND_CHOICES, blank=True, null=True)
    material = models.CharField(max_length=32, choices=MATERIAL_CHOICES, blank=True, null=True)
    gender = models.CharField(max_length=16, choices=GENDER_CHOICES, blank=True, null=True)
    age = models.CharField(max_length=16, choices=AGE_CHOICES, blank=True, null=True)
    color = models.CharField(max_length=16, choices=COLOR_CHOICES, blank=True, null=True)
    temple_size = models.IntegerField(blank=True, null=True)
    lens_width = models.IntegerField(blank=True, null=True)
    bridge_width = models.IntegerField(blank=True, null=True)
    category = models.ForeignKey(Category, related_name="products", on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:  # Генерируем только для новых объектов
            self.slug = self._generate_unique_slug()
            #self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def _generate_unique_slug(self):
        """Генерирует уникальный slug из имени, добавляя номер при необходимости"""
        base_slug = slugify(self.name)
        slug = base_slug
        num = 1
        
        while Product.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{num}"
            num += 1
            
        return slug

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name='carts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart #{self.pk} ({self.user})"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} x {self.quantity} (Cart #{self.cart_id})"
    
    @property
    def total_price(self):
        return self.product.price * self.quantity

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=32, default='new')

    def __str__(self):
        return f"Order #{self.pk} ({self.user})"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} x {self.quantity} (Order #{self.order_id})"
