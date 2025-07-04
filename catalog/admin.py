from django.contrib import admin
from .models import Category, Product, ProductImage

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'stock', 'external_id_display', 'image_preview']
    readonly_fields = ['image_preview']

    def image_preview(self, obj):
        if obj.image and hasattr(obj.image, 'image') and obj.image.image:
            from django.utils.html import mark_safe
            return mark_safe(f'<img src="{obj.image.image.url}" style="max-height: 100px;" />')
        return "-"
    image_preview.short_description = "Image Preview"

    def external_id_display(self, obj):
        return obj.external_id
    external_id_display.short_description = "Код 1С"

admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(ProductImage)