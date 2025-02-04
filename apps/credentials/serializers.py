from rest_framework import serializers
from .models import Category, Credential, UserCategory


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            "id",
            'uuid',
            'name',
            'icon'
        )


class UserCategorySerializer(serializers.ModelSerializer):
    class Meta(CategorySerializer.Meta):
        model = UserCategory


class CredentialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Credential
        fields = [
            "id",
            "user",
            "category",
            "user_category",
            "username",
            "password",
            "website",
            "notes",
        ]
        extra_kwargs = {
            "category": {"write_only": True, "required": False},
            "user_category": {"write_only": True, "required": False},
        }

    def validate(self, data):
        if self.instance is None:
            category = data.get("category")
            user_category = data.get("user_category")

            if not category and not user_category:
                raise serializers.ValidationError(
                    "Either `category` or `user_category` must be provided."
                )

        return data

    def to_representation(self, instance):
        request = self.context.get("request")
        representation = super().to_representation(instance)

        representation["category_data"] = {"custom": False}

        if instance.category:
            icon_url = instance.category.icon.url if instance.category.icon else None
            if icon_url and request:
                icon_url = request.build_absolute_uri(icon_url)
            representation["category_data"] = {
                "icon": icon_url,
                "name": instance.category.name,
                "uuid": str(instance.category.uuid),
            }
        elif instance.user_category:
            icon_url = (
                instance.user_category.icon.url
                if instance.user_category.icon
                else None
            )
            if icon_url and request:
                icon_url = request.build_absolute_uri(icon_url)
            representation["category_data"] = {
                "custom": True,
                "icon": icon_url,
                "name": instance.user_category.name,
                "uuid": str(instance.user_category.uuid),
            }

        return representation