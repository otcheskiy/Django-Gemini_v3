# catalog/views/products.py
from rest_framework import generics, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from catalog.serializers import ProductSerializer, ProductImageSerializer
from catalog.models import Product, ProductImage

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

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def create(self, request, *args, **kwargs):
        external_id = request.data.get('external_id')
        if external_id:
            try:
                instance = Product.objects.get(external_id=external_id)
                serializer = self.get_serializer(instance, data=request.data, partial=True)
                serializer.is_valid(raise_exception=True)
                self.perform_update(serializer)
                return Response(serializer.data, status=200)
            except Product.DoesNotExist:
                pass
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)

class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer

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
        for k, v in data.items():
            filtered = [x for x in v if x not in [None, '']]
            data[k] = sorted(filtered)
        return Response(data) 