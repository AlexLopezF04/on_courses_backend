from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    path('admin/', admin.site.urls),

    # Documentación de la API
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # Módulos de la API
    path('api/', include('apps.users.urls')),
    path('api/', include('apps.courses.urls')),
    path('api/', include('apps.community.urls')),
    path('api/', include('apps.progress.urls')),
    path('api/', include('apps.gamification.urls')),
    path('api/', include('apps.commercial.urls')),
]
