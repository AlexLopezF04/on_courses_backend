from decimal import Decimal

from django.utils.timezone import now
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from courses.filters import OrderFilter
from courses.models import Cart, Order, OrderItem
from courses.permissions import IsAdminOrSelfForOrder, IsAdminUser
from courses.serializers import OrderSerializer, OrderWriteSerializer


class OrderViewSet(viewsets.ModelViewSet):
    """CRUD de órdenes de compra."""

    queryset = Order.objects.all()
    filterset_class = OrderFilter
    ordering_fields = ["created_at"]

    def get_serializer_class(self):
        if self.action in ("create",):
            return OrderWriteSerializer
        return OrderSerializer

    def get_permissions(self):
        if self.action in ("list",):
            return [IsAdminUser()]
        if self.action in ("retrieve",):
            return [IsAuthenticated(), IsAdminOrSelfForOrder()]
        if self.action in ("update", "partial_update", "destroy"):
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def get_queryset(self):
        if self.request.user.role == "admin":
            return Order.objects.all()
        return Order.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        coupon = serializer.validated_data.get("coupon")

        cart, _ = Cart.objects.get_or_create(user=user)
        cart_items = cart.items.all()

        if not cart_items:
            return Response({"error": "El carrito está vacío"}, status=status.HTTP_400_BAD_REQUEST)

        total = sum(item.course.price for item in cart_items)

        if coupon:
            if coupon.discount_type == "percentage":
                total -= total * (coupon.discount_value / Decimal(100))
            elif coupon.discount_type == "fixed":
                total -= coupon.discount_value
            coupon.current_uses += 1
            coupon.save()

        order = serializer.save(user=user, total=max(total, 0))

        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order, course=cart_item.course, unit_price=cart_item.course.price
            )

        cart_items.delete()

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"])
    def pay(self, request, pk=None):
        """Simula el pago de una orden (cambia estado a 'paid')."""
        order = self.get_object()
        if order.status != "pending":
            return Response(
                {"error": "La orden no está pendiente"}, status=status.HTTP_400_BAD_REQUEST
            )
        order.status = "paid"
        order.paid_at = now()
        order.save()
        return Response(OrderSerializer(order).data)
