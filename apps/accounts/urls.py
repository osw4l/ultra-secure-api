from django.urls import path, include
from rest_framework import routers
from . import views, viewsets

app_name = 'accounts'


router = routers.DefaultRouter()
router.register(r'create', viewsets.CreateAccountViewSet)

urlpatterns = [
    path('user/', views.UserDetailView.as_view(), name='user_detail'),
    path('', include(router.urls)),
]
