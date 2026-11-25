from rest_framework import serializers
from .models import Brand, Frame, Review


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name', 'logo']


class FrameSerializer(serializers.ModelSerializer):
    brand = serializers.StringRelatedField()

    class Meta:
        model = Frame
        fields = ['id', 'brand', 'name', 'price', 'image', 'description', 'in_stock']


class ReviewSerializer(serializers.ModelSerializer):
    customer = serializers.CharField(source='order.customer.user.first_name', read_only=True)
    frame = serializers.CharField(source='order.frame.name', read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'customer', 'frame', 'rating', 'feedback', 'created']