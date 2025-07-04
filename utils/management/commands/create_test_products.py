# utils/management/commands/create_test_products.py

from django.core.management.base import BaseCommand
from catalog.models import Product, Category
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Создаёт тестовые товары'

    def handle(self, *args, **kwargs):
        cat, _ = Category.objects.get_or_create(name="Оправы")

        for i in range(1, 5):
            name = f"Оправа {i}"
            code = f"УТ0000{i:03d}"
            unique_slug = slugify(f"{name}-{i}-{name}")

            product = Product.objects.create(
                name=name,
                price=1000 * i,
                stock=10 + i,
                code_1c=code,
                #slug=slugify(name),
                slug=unique_slug,
            )
            product.categories.add(cat)
            self.stdout.write(self.style.SUCCESS(f'✅ Товар "{name}" создан'))

        self.stdout.write(self.style.SUCCESS("Все товары успешно добавлены"))