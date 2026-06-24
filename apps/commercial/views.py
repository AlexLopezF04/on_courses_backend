from decimal import Decimal
from django.utils.timezone import now
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from apps.commercial.models import Cart, CartItem, Coupon, Order, OrderItem, SupportTicket, SupportMessage
from apps.commercial.serializers import (
    CartSerializer, CartItemSerializer, CartItemWriteSerializer,
    CouponSerializer,
    OrderSerializer, OrderWriteSerializer, OrderItemSerializer,
    SupportTicketSerializer, SupportTicketWriteSerializer,
    SupportMessageSerializer
)
from apps.commercial.filters import OrderFilter, SupportTicketFilter
from apps.commercial.permissions import IsOwnerOfTicket, IsAdminOrSelfForOrder
from apps.users.permissions import IsAdminUser


class CartViewSet(viewsets.ModelViewSet):
    """Carrito de compras. Un carrito por usuario."""
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def get_permissions(self):
        if self.action in ('list',):
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def get_queryset(self):
        if self.request.user.role == 'admin':
            return Cart.objects.all()
        return Cart.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get'])
    def mine(self, request):
        """Obtiene o crea el carrito del usuario autenticado."""
        cart, _ = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)


class CartItemViewSet(viewsets.ModelViewSet):
    """Ítems del carrito. Agregar/remover cursos."""
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    def get_serializer_class(self):
        if self.action in ('create',):
            return CartItemWriteSerializer
        return CartItemSerializer

    def get_permissions(self):
        return [IsAuthenticated()]

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)

    def perform_create(self, serializer):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        serializer.save(cart=cart)


class CouponViewSet(viewsets.ModelViewSet):
    """CRUD de cupones. Solo administradores."""
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    search_fields = ['code']

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return [AllowAny()]
        return [IsAdminUser()]

    @action(detail=False, methods=['get'])
    def validate(self, request):
        """Valida un código de cupón."""
        code = request.query_params.get('code', '')
        try:
            coupon = Coupon.objects.get(code=code, is_active=True)
            return Response({
                'valid': True,
                'discount_type': coupon.discount_type,
                'discount_value': coupon.discount_value
            })
        except Coupon.DoesNotExist:
            return Response({'valid': False, 'error': 'Cupón inválido o expirado'})


class OrderViewSet(viewsets.ModelViewSet):
    """CRUD de órdenes de compra."""
    queryset = Order.objects.all()
    filterset_class = OrderFilter
    ordering_fields = ['created_at']

    def get_serializer_class(self):
        if self.action in ('create',):
            return OrderWriteSerializer
        return OrderSerializer

    def get_permissions(self):
        if self.action in ('list',):
            return [IsAdminUser()]
        if self.action in ('retrieve',):
            return [IsAuthenticated(), IsAdminOrSelfForOrder()]
        if self.action in ('update', 'partial_update', 'destroy'):
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def get_queryset(self):
        if self.request.user.role == 'admin':
            return Order.objects.all()
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        user = self.request.user
        coupon = serializer.validated_data.get('coupon')

        # Obtiene items del carrito
        cart, _ = Cart.objects.get_or_create(user=user)
        cart_items = cart.items.all()

        if not cart_items:
            return Response(
                {'error': 'El carrito está vacío'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Calcula el total
        total = sum(item.course.price for item in cart_items)

        # Aplica descuento si hay cupón
        if coupon:
            if coupon.discount_type == 'percentage':
                total -= total * (coupon.discount_value / Decimal(100))
            elif coupon.discount_type == 'fixed':
                total -= coupon.discount_value
            coupon.current_uses += 1
            coupon.save()

        order = serializer.save(user=user, total=max(total, 0))

        # Crea los items de la orden
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                course=cart_item.course,
                unit_price=cart_item.course.price
            )

        # Vacía el carrito
        cart_items.delete()

    @action(detail=True, methods=['post'])
    def pay(self, request, pk=None):
        """Simula el pago de una orden (cambia estado a 'paid')."""
        order = self.get_object()
        if order.status != 'pending':
            return Response(
                {'error': 'La orden no está pendiente'},
                status=status.HTTP_400_BAD_REQUEST
            )
        order.status = 'paid'
        order.paid_at = now()
        order.save()
        return Response(OrderSerializer(order).data)


class SupportTicketViewSet(viewsets.ModelViewSet):
    """CRUD de tickets de soporte."""
    queryset = SupportTicket.objects.all()
    filterset_class = SupportTicketFilter
    search_fields = ['subject', 'description']

    def get_serializer_class(self):
        if self.action in ('create',):
            return SupportTicketWriteSerializer
        return SupportTicketSerializer

    def get_permissions(self):
        if self.action in ('list',):
            return [IsAdminUser()]
        if self.action in ('retrieve', 'update', 'partial_update'):
            return [IsAuthenticated(), IsOwnerOfTicket()]
        return [IsAuthenticated()]

    def get_queryset(self):
        if self.request.user.role == 'admin':
            return SupportTicket.objects.all()
        return SupportTicket.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def add_message(self, request, pk=None):
        """Agrega un mensaje a un ticket existente."""
        ticket = self.get_object()
        message_text = request.data.get('message', '')
        if not message_text:
            return Response(
                {'error': 'El mensaje no puede estar vacío'},
                status=status.HTTP_400_BAD_REQUEST
            )

        message = SupportMessage.objects.create(
            ticket=ticket,
            sender=request.user,
            message=message_text
        )
        return Response(SupportMessageSerializer(message).data)
