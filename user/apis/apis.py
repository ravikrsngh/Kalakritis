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
                try:
                    instance = self.queryset.get(email=serializer.validated_data['email'])
                except Exception as e:
                    return Response({"details":"User does not exists."}, status=status.HTTP_400_BAD_REQUEST)
                otp = send_OTP_email(email)
                instance.temp_otp = otp
                instance.save()
                return Response({"details":"Email Sent"})
            except Exception as e:
                print(e)
                return Response({"details":"Some error while sending OTP"})

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
