# catalog/serializers.py
from rest_framework import serializers
from .models import Product, Category, ProductImage

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'uploaded_at']

class ProductSerializer(serializers.ModelSerializer):
    external_id = serializers.CharField(
        required=True,
        allow_blank=False,
        error_messages={
            "blank": "Поле external_id обязательно для заполнения.",
            "required": "Поле external_id обязательно для заполнения."
        }
    )
    image = serializers.PrimaryKeyRelatedField(queryset=ProductImage.objects.all(), required=False, allow_null=True)
    image_url = serializers.SerializerMethodField()
    category_id = serializers.PrimaryKeyRelatedField(source='category', queryset=Category.objects.all(), required=False, allow_null=True)
    category_name = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'price', 'stock', 'external_id', 'image', 'image_url',
            'brand', 'material', 'gender', 'age', 'color',
            'temple_size', 'lens_width', 'bridge_width',
            'category_id', 'category_name', 'slug'
        ]

    def get_image_url(self, obj):
        if obj.image and obj.image.image:
            request = self.context.get('request')
            url = obj.image.image.url
            if request is not None:
                return request.build_absolute_uri(url)
            return url
        return None

    def get_category_name(self, obj):
        return obj.category.name if obj.category else None

    def create(self, validated_data):
        categories = validated_data.pop('categories', [])
        external_id = validated_data.get('external_id')
        instance = None
        if external_id:
            instance = Product.objects.filter(external_id=external_id).first()
        if instance:
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()
            if categories:
                instance.categories.set(categories)
            return instance
        instance = Product(**validated_data)
        instance.save()
        if categories:
            instance.categories.set(categories)
        return instance

    def update(self, instance, validated_data):
        categories = validated_data.pop('categories', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if categories is not None:
            instance.categories.set(categories)
        return instance