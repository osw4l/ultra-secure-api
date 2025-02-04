from rest_framework import viewsets, mixins, permissions, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.accounts.models import Account, RecoveryPin
from apps.accounts.serializers import AccountRegisterSerializer, AccountSerializer, AccountResetPasswordSerializer, \
    AccountCodeValidatorSerializer, AccountSetNewPasswordSerializer


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


class AccountRecoveryViewSet(CreateAccountViewSet):
    @action(detail=False,
            methods=['POST'],
            permission_classes=[AllowAny],
            serializer_class=AccountResetPasswordSerializer)
    def send_reset_code(self, request):
        email = request.data.get('email')
        account = get_object_or_404(Account, email=email)
        account.generate_recovery_code()

        return Response()

    @action(detail=False,
            permission_classes=[AllowAny],
            methods=['POST'],
            serializer_class=AccountCodeValidatorSerializer)
    def validate_reset_code(self, request):
        email = request.data.get('email')
        code = request.data.get('code')
        get_object_or_404(RecoveryPin, user__email=email, code=code)
        return Response()

    @action(detail=False,
            methods=['POST'],
            permission_classes=[AllowAny],
            serializer_class=AccountSetNewPasswordSerializer)
    def change_password(self, request):
        email = request.data.get('email')
        code = request.data.get('code')
        password = request.data.get('password')
        pin = get_object_or_404(RecoveryPin, user__email=email, code=code)
        pin.user.set_new_password(password=password)
        return Response()