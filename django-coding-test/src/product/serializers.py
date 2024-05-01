from rest_framework import serializers
from .models import Product, Variant

class ProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class VariantSerializers(serializers.ModelSerializer):
    class Meta:
        model = Variant
        fields = '__all__'