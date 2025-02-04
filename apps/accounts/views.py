from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets

from apps.accounts.models import Account
from apps.accounts.serializers import AccountSerializer


class UserDetailView(RetrieveAPIView):
    serializer_class = AccountSerializer

    def get_object(self):
        return Account.objects.get(
            pk=self.request.user.pk
        )
