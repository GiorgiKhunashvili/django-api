from rest_framework import serializers
from .models import UserAccount


class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ['id', 'email', 'username', 'name']


class ResetPassowrdEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class UserRegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = UserAccount
        fields = ['email', 'username', 'name', 'password', 'confirm_password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        user_account = UserAccount(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
            name=self.validated_data['name']
        )
        password = self.validated_data['password']
        confirm_password = self.validated_data['confirm_password']

        if password != confirm_password:
            raise serializers.ValidationError({"password": "passwords must match!"})
        user_account.set_password(password)
        user_account.save()
        return user_account


class ChanagePasswordSerializer(serializers.Serializer):
    """serializer for password change"""
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class DeleteUserSerializer(serializers.Serializer):
    """serializer for deleting user"""
    password = serializers.CharField(required=True)
