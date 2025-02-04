from rest_framework import serializers
from .models import Account
from ..credentials.serializers import UserCategorySerializer


class AccountSerializer(serializers.ModelSerializer):
    categories = UserCategorySerializer(read_only=True, many=True)

    class Meta:
        model = Account
        fields = ['uuid', 'email', 'first_name', 'last_name', 'categories',]
        depth = 1


class AccountRegisterSerializer(AccountSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        help_text='Leave empty if no change needed',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )

    class Meta(AccountSerializer.Meta):
        fields = AccountSerializer.Meta.fields + ["password",]


class AccountResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class AccountEmailResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class CodeSerializer(AccountResetPasswordSerializer):
    code = serializers.CharField(min_length=4, max_length=4)


class AccountCodeValidatorSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True,
    )
    code = serializers.CharField(min_length=4, max_length=4)


class AccountSetNewPasswordSerializer(AccountCodeValidatorSerializer):
    password = serializers.CharField(min_length=6)


