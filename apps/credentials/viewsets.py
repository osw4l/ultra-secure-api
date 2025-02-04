from rest_framework import viewsets, permissions, mixins, filters

from .models import Category, UserCategory, Credential
from .serializers import CategorySerializer, UserCategorySerializer, CredentialSerializer


class CategoryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated, ]


class UserCategoryViewSet(mixins.ListModelMixin,
                          mixins.CreateModelMixin,
                          mixins.DestroyModelMixin,
                          viewsets.GenericViewSet):
    queryset = UserCategory.objects.all()
    serializer_class = UserCategorySerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CredentialViewSet(viewsets.ModelViewSet):
    queryset = Credential.objects.all().select_related('user', 'category', 'user_category')
    serializer_class = CredentialSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = [
        'username',
        'website',
        'notes',
        'category__name',
        'user_category__name',
    ]

    def get_queryset(self):
        qs = super().get_queryset()
        category = self.request.query_params.get('category', None)
        user_category = self.request.query_params.get('user_category', None)
        kwargs = {
            'user': self.request.user
        }
        if category:
            kwargs['category'] = category
        if user_category:
            kwargs['user_category'] = user_category

        return qs.filter(**kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

