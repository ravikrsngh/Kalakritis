from typing import Any, Dict, Optional, Type, TypeVar

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import viewsets, status



from user.models import *
from .serializers import *
from services.emails import *


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['email'] = user.email
        token['fullname'] = f'{user.first_name} {user.last_name}'

        return token

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        data = super().validate(attrs)
        data['user'] = self.user.id
        data["fullname"] = f'{self.user.first_name} {self.user.last_name}'
        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class UserAPI(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()

    def get_serializer_class(self):
        if self.action == 'partial_update':
            return UserUpdateSerializer
        if self.action == "create":
            return UserCreateSerializer
        return UserDetailsSerializer

    def set_password(self, instance, password):
        instance.set_password(password)
        instance.save()

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # if not serializer.validated_data['password'] == serializer.validated_data['confirm_password']:
        #     return Response({"details":"The passwords dont match."}, status=status.HTTP_400_BAD_REQUEST)
        instance = serializer.save()
        self.set_password(instance, instance.password)
        instance_serializer = UserDetailsSerializer(instance)
        return Response(instance_serializer.data)

    @action(methods=['post'], detail=False)
    def send_otp(self,request):
        serializer = SendOTPSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                email = serializer.validated_data['email']
                if self.queryset.filter(email=serializer.validated_data['email']).exists():
                    instance = self.queryset.get(email=serializer.validated_data['email'])
                else:
                    instance = TemperaryOTP.objects.create(email=email)
                otp = send_OTP_email(email)
                instance.temp_otp = otp
                instance.save()
                return Response({"details":"Email Sent"})
            except Exception as e:
                print(e)
                return Response({"details":"Some error while sending OTP"}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False)
    def verify_otp_for_create(self,request):
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            if TemperaryOTP.objects.filter(email=serializer.validated_data['email']).filter(temp_otp=serializer.validated_data['otp']).exists():
                TemperaryOTP.objects.filter(email=serializer.validated_data['email']).delete()
                return Response({"details":"Verfied"})
            else:
                return Response({"details":"Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False)
    def set_new_password(self, request, pk=None):
        serializer = SetNewPasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                instance = self.queryset.get(email=serializer.validated_data['email'])
            except Exception as e:
                return Response({"details":"User does not exists."}, status=status.HTTP_400_BAD_REQUEST)
            if serializer.validated_data['new_password'] == serializer.validated_data['confirm_new_password']:
                if instance.temp_otp == serializer.validated_data['otp']:
                    self.set_password(instance, serializer.validated_data['confirm_new_password'])
                    return Response({"details":"Password Changed Successfully."})
                return Response({"details":"Enter the correct OTP"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"details":"New Password and Confirm New Password does not match."}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False)
    def check_user_exists(self,request):
        if CustomUser.objects.filter(email=request.data.get('email',None)).exists():
            return Response({"user_exists":True})
        else:
            return Response({"user_exists":False})



class UserAddressAPI(viewsets.ModelViewSet):
    queryset = UserAddress.objects.all()
    serializer_class = UserAddressSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return UserAddress.objects.filter(user=self.request.user)
        return []

    def create(self, request):
        if self.request.user.is_authenticated:
            request.data['user'] = self.request.user.id
            return super().create(request)
        else:
            return Response({"details":"User is not authenticated."}, status=status.HTTP_400_BAD_REQUEST)
