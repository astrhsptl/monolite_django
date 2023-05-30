"""server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

from .settings import DEBUG

from django.conf.urls.static import static
from django.views.static import serve
from django.conf import settings



schema_view = get_schema_view(
    openapi.Info(
        title="API",
        default_version='v1',
        description="API documentation",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('', include('pages.urls')),
    path('', include('authsystem.urls')),
    path('admin/', admin.site.urls),
    path('api/v1/docs/', include('APIpoints.urls')),
] 

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


'''
[
path('', schema_view.with_ui('swagger', cache_timeout=0), name="swagger-schema"),
path('api.json/', schema_view.without_ui(cache_timeout=0), name='schema-swagger-ui'),
path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
path('', include('APIpoints.urls')),
])
'''

# if DEBUG:
#     import debug_toolbar

#     urlpatterns += [
#         path('__debug__/', include(debug_toolbar.urls)),
#     ]
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# else:
#     urlpatterns += [
#         static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#         # path(f'^{settings.MEDIA_URL.lstrip("/")}(?P<path>.*)$',
#         #     serve, {'document_root': settings.MEDIA_ROOT}),
#         # path(f'^{settings.STATIC_URL.lstrip("/")}(?P<path>.*)$',
#         #     serve, {'document_root': settings.STATIC_ROOT}),
#     ]
