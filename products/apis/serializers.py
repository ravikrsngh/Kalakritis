from products.models import *
from rest_framework import serializers


class ProductImageSerializer(serializers.ModelSerializer):
    img = serializers.ImageField(required=False)

    class Meta:
        model = ProductImages
        fields = ['id','img','order']

class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductTypes
        fields = ['id','name']

class ColorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Colors
        fields = ['id','name','hash_value']

class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ['id','name']

class SizesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sizes
        fields = ['id','name']


class ProductSerializer(serializers.ModelSerializer):
    product_images = ProductImageSerializer(many=True)
    product_type = ProductTypeSerializer(many=False)
    colors = ColorsSerializer(many=True)
    tags = TagsSerializer(many=True)
    sizes = SizesSerializer(many=True)
    discount_percent = serializers.SerializerMethodField()
    is_wishlisted = serializers.BooleanField(read_only=True)

    def get_discount_percent(self, obj):
        return int((obj.cost_price - obj.selling_price)*100/obj.cost_price)

    # def to_representation(self, instance):
    #     # Get the product images for the current product instance
    #     product_images = instance.product_images.all().order_by('order')
    #
    #     # Serialize the product images using the ProductImageSerializer
    #     serialized_product_images = ProductImageSerializer(product_images, many=True).data
    #
    #     # Add the serialized product images to the serialized product instance
    #     data = super().to_representation(instance)
    #     data['product_images'] = serialized_product_images
    #
    #     return data

    class Meta:
        model = Product
        fields = '__all__'
