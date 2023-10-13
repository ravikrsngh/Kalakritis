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


class OrderProductSerializer(serializers.ModelSerializer):
    size = serializers.CharField(max_length=5, required=True)
    color = serializers.CharField(max_length=50, required=True)
    class Meta:
        model = OrderProduct
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        exclude = ['created_date']
