from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from courses.models import Coupon
from courses.permissions import IsAdminUser
from courses.serializers import CouponSerializer


class CouponViewSet(viewsets.ModelViewSet):
    """CRUD de cupones. Solo administradores."""

    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    search_fields = ["code"]

    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            return [AllowAny()]
        return [IsAdminUser()]

    @action(detail=False, methods=["get"])
    def validate(self, request):
        """Valida un código de cupón."""
        code = request.query_params.get("code", "")
        try:
            coupon = Coupon.objects.get(code=code, is_active=True)
            return Response(
                {
                    "valid": True,
                    "discount_type": coupon.discount_type,
                    "discount_value": coupon.discount_value,
                }
            )
        except Coupon.DoesNotExist:
            return Response({"valid": False, "error": "Cupón inválido o expirado"})
