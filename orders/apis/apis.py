from rest_framework import viewsets, status
from .serializers import *
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.pagination import PageNumberPagination
from django_filters import rest_framework as filters
from datetime import datetime, timedelta
from rest_framework.permissions import IsAuthenticated
from converters import *
from utils import *
import requests
import environ


environ.Env.read_env()
env = environ.Env()


class CartAPI(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartDetailsSerializer
    permission_classes = [IsAuthenticated]

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

        #Calculate subtotal and no of items
        subtotal = 0
        no_of_items = 0
        for cart_item in response_data['cart_items']:
            subtotal += cart_item["product"]["selling_price"] * cart_item['qty']
            no_of_items += cart_item['qty']

        response_data['no_of_items'] = no_of_items
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
                    return Response({"details":"Product was already in the cart. So we have increased the quantity by 1."})
                else:
                    instance = serializer.save()
                    return Response({"details":"Added to Cart"})
        return Response({"details":"User is not logged in."}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'],detail=False)
    def buy_now(self, request):
        user = self.request.user
        if user.is_authenticated:
            Cart.objects.filter(user=user).delete()
            request.data['user'] = user.id
            serializer=AddToCartSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                instance = serializer.save()
                return Response()
        return Response({"details":"User is not logged in."}, status=status.HTTP_400_BAD_REQUEST)


    def list(self, request):
        user = self.request.user
        if user.is_authenticated:
            response = self.prepare_cart_data()
            coupon_name = request.GET.get('coupon',None)
            if coupon_name:
                self.apply_coupon_code(response,coupon_name)
            return Response(response)
        return {}


    def partial_update(self, request, pk=None):
        instance = self.get_object()
        instance.qty = request.data['qty']
        instance.save()
        return Response()


    def destroy(self, request, pk=None):
        super().destroy(request, pk=None)
        return Response()

    def apply_coupon_code(self,response, coupon_name):
        if CouponCodes.objects.filter(name__iexact=coupon_name).exists():
            coupon_instance = CouponCodes.objects.filter(name__iexact=coupon_name).first()
            response['coupon_details']['coupon_name'] = coupon_name
            response['coupon_details']['coupon_percent'] = coupon_instance.discount_perecent
            response['coupon_details']['coupon_discount'] = int((response['subtotal'] * response['coupon_details']['coupon_percent'])/100)
            response['coupon_details']["coupon_success_message"] = f'Coupon {coupon_name} applied - Rs. {response["coupon_details"]["coupon_discount"]}/- off.'
            response['total'] = response['total'] - response['coupon_details']['coupon_discount']
        else:
            response['coupon_details']["coupon_error_message"] = "Invalid coupon code."


class WishlistAPI(viewsets.ModelViewSet):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer
    permission_classes = [IsAuthenticated]

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
                return Response({"details":"Product already added to the wishlist."}, status=status.HTTP_400_BAD_REQUEST)
            serializer = WishlistSerializer(data = request.data)
            if serializer.is_valid(raise_exception=True):
                instance = serializer.save()
                return Response({"details":"Added to wishlist"})
        else:
            return Response({"details":"User is not logged in."}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=False)
    def get_product_ids(self, request):
        user = self.request.user
        if user.is_authenticated:
            return Response({
                "product_ids": Wishlist.objects.filter(user=user).values_list('product', flat=True)
            })
        return Response({"details":"User is not logged in."}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        Wishlist.objects.filter(user=self.request.user).filter(product__id=pk).delete()
        return Response()


class PhonePeAPI(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request):

        serializer = GetPaymentLinkSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):

            merchantTransactionId = generate_random_string(8)

            base_url = env('BASE_URL_FOR_REDIRECT')
            callbackUrl = base_url + "/phonepe-callback-url/"

            payload_for_base64 = {
              "merchantId": env('MID'),
              "merchantTransactionId": merchantTransactionId,
              "merchantUserId": request.user.id,
              "amount": serializer.validated_data['amount']*100,
              "redirectUrl": base_url + "/phonepe-redirect-url/"+merchantTransactionId+'/',
              "redirectMode": "GET",
              "callbackUrl": callbackUrl,
              "mobileNumber": request.user.phone_number,
              "paymentInstrument": {
                "type": "PAY_PAGE"
              }
            }

            url = env('INITIATE_PAY_URL')
            payload = {
                "request": dict_to_base64(payload_for_base64)
            }
            headers = {
                "Content-Type":"application/json",
                "X-VERIFY": toSHA256(payload['request']+'/pg/v1/pay'+env('SALT_KEY')) + "###"+ env('SALT_INDEX')
            }

            response = requests.post(url, headers=headers, json=payload)

            print(response.headers)

            return Response(response.json()['data']['instrumentResponse'])

    @action(detail=False, methods=['post'])
    def check_transaction_status(self, request):
        trx_id = request.data.get('trx_id', None)
        if trx_id is not None:

            check_status_url = env('CHECKSTATUS_URL')+ "/" + env('MID')+ "/" + trx_id
            print(check_status_url)
            headers = {
                "Content-Type":"application/json",
                "X-VERIFY": toSHA256(f"/pg/v1/status/{env('MID')}/{trx_id}"+env('SALT_KEY')) + "###"+ env('SALT_INDEX'),
                "X-MERCHANT-ID":env('MID')
            }

            response = requests.get(check_status_url, headers=headers)

            print(response.headers)
            res = response.json()
            del res['data']['merchantId']
            return Response(res)

        else:
            return Response({"details":"Transaction ID not found"}, status=status.HTTP_400_BAD_REQUEST)


class OrderAPI(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request):
        user = self.request.user
        ordered_products = request.data.pop('ordered_products')
        request.data['user'] = user.id
        order_serializer = OrderSerializer(data=request.data)
        if order_serializer.is_valid(raise_exception=True):
            order_instance = order_serializer.save()
            for ordered_product in ordered_products:
                ordered_product['order'] = order_instance.id
                ordered_product_serializer = OrderProductSerializer(data=ordered_product)
                try:
                    if ordered_product_serializer.is_valid(raise_exception=True):
                        ordered_product_instance = ordered_product_serializer.save()
                    Cart.objects.filter(user=user).delete()
                except Exception as e:
                    order_instance.delete()
                    raise

        return Response({"details":"Order created."})
