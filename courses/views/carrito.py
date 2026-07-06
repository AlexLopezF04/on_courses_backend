from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from courses.models import Cart, CartItem
from courses.permissions import IsAdminUser
from courses.serializers import CartSerializer, CartItemSerializer, CartItemWriteSerializer


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
