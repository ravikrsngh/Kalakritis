from rest_framework import viewsets, status
from .serializers import *
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.pagination import PageNumberPagination
from django_filters import rest_framework as filters
from datetime import datetime, timedelta


class CartAPI(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = WishlistSerializer

    def prepare_cart_data(self):
        response_data = {
            "no_of_items":0,
            "subtotal":0,
            "delivery_charges": "Free",
            "tax": 0,
            "coupon_details":{
                "coupon_name":None,
                "coupon_percent":0,
                "coupon_discount": 0,
                "coupon_success_message":None,
                "coupon_error_message":None
            },
            "total":0,
            "cart_items":[]
        }
        queryset = self.get_queryset()
        serializer = CartDetailsSerializer(queryset, many=True)
        response_data['cart_items'] = serializer.data
        response_data['no_of_items'] = len(response_data['cart_items'])
        #Calculate subtotal
        subtotal = 0
        for cart_item in response_data['cart_items']:
            subtotal += cart_item["product"]["selling_price"] * cart_item['qty']

        response_data['subtotal'] = subtotal
        response_data['tax'] = int((subtotal * 18)/100)
        response_data['total'] = response_data['subtotal'] + response_data['tax']
        return response_data


    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Cart.objects.select_related('product').filter(user=user)
        return []


    def create(self,request):
        user = self.request.user
        if user.is_authenticated:
            request.data['user'] = user.id
            serializer=AddToCartSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                if Cart.objects.filter(user=user).filter(product=serializer.validated_data['product']).filter(color=serializer.validated_data['color']).filter(size=serializer.validated_data['size']).exists():
                    instance = Cart.objects.get(user=user,product=serializer.validated_data['product'],color=serializer.validated_data['color'],size=serializer.validated_data['size'])
                    instance.qty = instance.qty + 1
                    instance.save()
                    return Response({"details":"Product was already in the cart. So we have increased the quantity by 1."}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    instance = serializer.save()
                    return Response({"details":"Added to Cart"})
        return Response({"details":"User is not logged in."}, status=status.HTTP_400_BAD_REQUEST)


    def list(self, request):
        user = self.request.user
        if user.is_authenticated:
            response = self.prepare_cart_data()
            return Response(response)
        return {}


    def partial_update(self, request, pk=None):
        instance = self.get_object()
        instance.qty = request.data['qty']
        instance.save()
        response = self.prepare_cart_data()
        return Response(response)


    def destroy(self, request, pk=None):
        super().destroy(request, pk=None)
        response = self.prepare_cart_data()
        return Response(response)


    @action(methods=['post'], detail=False)
    def apply_coupon_code(self, request):
        response = self.prepare_cart_data()
        coupon_name = request.data['coupon']
        if CouponCodes.objects.filter(name__iexact=coupon_name).exists():
            coupon_instance = CouponCodes.objects.filter(name__iexact=coupon_name).first()
            response['coupon_details']['coupon_name'] = coupon_name
            response['coupon_details']['coupon_percent'] = coupon_instance.discount_perecent
            response['coupon_details']['coupon_discount'] = int((response['subtotal'] * response['coupon_details']['coupon_percent'])/100)
            response['coupon_details']["coupon_success_message"] = f'{coupon_name} - Rs. {response["coupon_details"]["coupon_discount"]}/- off.'
            response['total'] = response['total'] - response['coupon_details']['coupon_discount']
        else:
            response['coupon_details']["coupon_error_message"] = "Invalid coupon code."
        return Response(response)


class WishlistAPI(viewsets.ModelViewSet):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer

    def get_queryset(self):
        user = self.request.user
        if user is not None:
            return Wishlist.objects.select_related('product').filter(user=user)
        return []

    def get_serializer_class(self):
        if self.action == 'list':
            return WishlistDetailsSerializer

    def create(self, request):
        user = self.request.user
        if user is not None:
            request.data['user'] = user.id
            if Wishlist.objects.filter(user=user).filter(product=request.data['product']).exists():
                return Response({"details":"Product already added to the wishlist."})
            serializer = WishlistSerializer(data = request.data)
            if serializer.is_valid(raise_exception=True):
                instance = serializer.save()
                return Response({"details":"Added to wishlist"})
        else:
            return Response({"details":"User is not logged in."}, status=status.HTTP_400_BAD_REQUEST)
