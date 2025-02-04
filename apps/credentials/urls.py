from django.urls import path, include
from .viewsets import CategoryViewSet, UserCategoryViewSet, CredentialViewSet
from rest_framework import routers

app_name = 'credentials'


router = routers.DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'user_categories', UserCategoryViewSet)
router.register(r'credentials', CredentialViewSet)

urlpatterns = [
    path('', include(router.urls))
]

