from rest_framework import serializers

from services.validations import *

from user.models import *


class UserCreateSerializer(serializers.ModelSerializer):

    confirm_password = serializers.CharField(max_length=16)

    def validate_password(self, value):
        print("Validating Password")
        if len(value) < 8:
            raise serializers.ValidationError("The Password should be between 8 and 16 characters.")
        return value

    def validate_phone_number(self, value):
        print("Validating Phone Number")
        if is_valid_phone_number(value):
            return value
        raise serializers.ValidationError("Enter a valid phone number.")

    class Meta:
        model = CustomUser
        fields = '__all__'


class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        exclude = ['password']


class UserUpdateSerializer(serializers.ModelSerializer):

    def validate_phone_number(self, value):
        print("Validating Phone Number")
        if is_valid_phone_number(value):
            return value
        raise serializers.ValidationError("Enter a valid phone number.")

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone_number']


class SendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()


class SetNewPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=4)
    new_password = serializers.CharField(max_length=16)
    confirm_new_password = serializers.CharField(max_length=16)

    def validate_new_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("The Password should be between 8 and 16 characters.")
        return value

    def validate_confirm_new_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("The Password should be between 8 and 16 characters.")
        return value


class UserAddressSerializer(serializers.ModelSerializer):

    def validate_phone_number(self, value):
        print("Validating Phone Number")
        if is_valid_phone_number(value):
            return value
        raise serializers.ValidationError("Enter a valid phone number.")

    class Meta:
        model = UserAddress
        fields = '__all__'
