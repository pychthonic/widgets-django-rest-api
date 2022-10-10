"""widgets URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path
from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from widgets import views


SchemaView = get_schema_view(
    openapi.Info(
        title="Widgets API",
        default_version='v1',
        description="Widgets Management",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,)
)

urlpatterns = [
    re_path('admin/', admin.site.urls),
    re_path(r'^(?P<version>\w{1,3})/widgets/id/(?P<id>\d+)',
            views.widget),
    re_path(r'^(?P<version>\w{1,3})/widgets/types', views.widget_types),
    re_path(r'^(?P<version>\w{1,3})/widgets/type/(?P<widget_type>\w+)',
            views.widgets),
    re_path(r'^(?P<version>\w{1,3})/widgets', views.widgets),
    path('swagger.json',
         SchemaView.without_ui(cache_timeout=0),
         name='schema-json'),
    path('swagger/', SchemaView.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path('redoc/', SchemaView.with_ui('redoc', cache_timeout=0),
         name='schema-redoc'),
]
