from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.commercial.views import (
    CartViewSet, CartItemViewSet, CouponViewSet,
    OrderViewSet, SupportTicketViewSet
)

router = DefaultRouter()
router.register(r'carts', CartViewSet)
router.register(r'cart-items', CartItemViewSet)
router.register(r'coupons', CouponViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'support-tickets', SupportTicketViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
