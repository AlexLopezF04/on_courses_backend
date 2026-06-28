from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.users.views import RegisterView, UserViewSet, health_check, LogoutView

router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    # Health check
    path('health/', health_check),

    # Autenticación JWT
    path('auth/register/', RegisterView.as_view()),
    path('auth/login/', TokenObtainPairView.as_view()),
    path('auth/refresh/', TokenRefreshView.as_view()),
    path('auth/logout/', LogoutView.as_view(), name='logout'),

    # CRUD de usuarios (vía router)
    path('', include(router.urls)),
]
