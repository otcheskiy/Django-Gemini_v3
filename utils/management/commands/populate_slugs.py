# utils/management/commands/populate_slugs.py

from django.core.management.base import BaseCommand
from catalog.models import Product
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Populate the slug field for existing products'

    def handle(self, *args, **options):
        products = Product.objects.all()
        for product in products:
            if not product.slug:
                product.slug = slugify(product.name)
                product.save()
        self.stdout.write(self.style.SUCCESS('Slugs populated successfully!'))