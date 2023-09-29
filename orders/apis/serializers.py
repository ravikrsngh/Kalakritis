from rest_framework import serializers
from orders.models import *
from products.apis.serializers import *


class WishlistSerializer(serializers.ModelSerializer):

    class Meta:
        model = Wishlist
        fields = '__all__'


class WishlistDetailsSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=False)
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
