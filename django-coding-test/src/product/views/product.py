from django.views import generic
from product.models import Variant, Product, ProductVariant
from rest_framework import viewsets
from django.db.models import Q
from datetime import datetime
from product.serializers import ProductSerializers, VariantSerializers


class CreateProductView(generic.TemplateView):
    template_name = 'products/create.html'

    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['product'] = True
        context['variants'] = list(variants.all())
        return context

class ProductView(generic.ListView):
    model = Product
    template_name = 'products/list.html'
    context_object_name = 'products'
    paginate_by = 2

    def get_queryset(self):
        queryset = super().get_queryset()
        title = self.request.GET.get('title')
        variant = self.request.GET.get('variant')
        price_from = self.request.GET.get('price_from')
        price_to = self.request.GET.get('price_to')
        date = self.request.GET.get('date')

        filters = Q()

        if title:
            filters &= Q(title__icontains=title)

        if variant:
            filters &= Q(productvariant__variant_title__icontains=variant)

        if price_from:
            filters &= Q(productvariantprice__price__gte=price_from)

        if price_to:
            filters &= Q(productvariantprice__price__lte=price_to)

        if date:
            try:
                date = datetime.strptime(date, '%Y-%m-%d')
                filters &= Q(created_at__date=date)
            except ValueError:
                pass  

        queryset = queryset.filter(filters).distinct()

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        variants = Variant.objects.all()
        unique_variants = {}
        for variant in variants:
            unique_variants[variant.title] = ProductVariant.objects.filter(variant=variant).values_list('variant_title', flat=True).distinct()
        context['unique_variants'] = unique_variants
        return context
    
class ProductAPIView(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers

    def custom_action(self, request, *args, **kwargs):
        pass