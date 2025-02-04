from rest_framework import viewsets, mixins, permissions, status
from rest_framework.response import Response

from apps.accounts.models import Account
from apps.accounts.serializers import AccountRegisterSerializer, AccountSerializer


class CreateAccountViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    serializer_class = AccountRegisterSerializer
    queryset = Account.objects.filter(deleted=False)
    permission_classes = [permissions.AllowAny, ]

    def perform_create(self, serializer):
        account = serializer.save()
        account.set_password(serializer.validated_data["password"])
        account.save()

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response(
            {"message": "Account successfully created!", "data": response.data},
            status=status.HTTP_201_CREATED
        )
