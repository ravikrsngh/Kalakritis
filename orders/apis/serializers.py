from rest_framework import serializers
from orders.models import *
from products.apis.serializers import *


class WishlistSerializer(serializers.ModelSerializer):

    class Meta:
        model = Wishlist
        fields = '__all__'


class WishlistDetailsSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=False)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['product']['is_wishlisted'] = True
        return data

    class Meta:
        model = Wishlist
        fields = ['id','product']


class AddToCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'

class CartDetailsSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=False)

    class Meta:
        model = Cart
        exclude = ['user']


class GetPaymentLinkSerializer(serializers.Serializer):
    amount = serializers.IntegerField()


class OrderProductDetailsSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()

    def get_product(self, instance):
        product_image = instance.product.product_images.all()[0]
        return {
            "sku" :  instance.product.sku,
            "title" : instance.product.title,
            "cost_price" : instance.product.cost_price,
            "selling_price" : instance.product.selling_price,
            "product_type" : instance.product.product_type.name,
            "img": product_image.img.url
        }

    class Meta:
        model = OrderProduct
        fields = '__all__'


class OrderDetailsSerializer(serializers.ModelSerializer):
    ordered_products = OrderProductDetailsSerializer(many=True)

    class Meta:
        model = Order
        fields = '__all__'


class OrderProductSerializer(serializers.ModelSerializer):
    size = serializers.CharField(max_length=5, required=True)
    color = serializers.CharField(max_length=50, required=True)
    class Meta:
        model = OrderProduct
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        exclude = ['created_date','paymentID','payment_status', 'payment_type_details']
