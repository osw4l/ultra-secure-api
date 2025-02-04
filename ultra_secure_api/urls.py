"""
URL configuration for ultra_secure_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.credentials.views import health

schema_view = get_schema_view(
    openapi.Info(
        title="Ultra-Secure API",
        default_version='v1',
        description="Project build by osw4l",
        contact=openapi.Contact(email="ioswxd@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('ultra-secure/admin/', admin.site.urls),
    path('ultra-secure/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('ultra-secure/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('ultra-secure/accounts/', include('apps.accounts.urls')),
    path('ultra-secure/credentials/', include('apps.credentials.urls')),
    path('ultra-secure/<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('ultra-secure/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('', health),
]
