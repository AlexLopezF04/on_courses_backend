from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOfTicket(BasePermission):
    """Solo el dueño del ticket o un admin pueden ver/modificar."""
    def has_object_permission(self, request, view, obj):
        if request.user.role == 'admin':
            return True
        return obj.user == request.user


class IsAdminOrSelfForOrder(BasePermission):
    """Solo el comprador o un admin pueden ver la orden."""
    def has_object_permission(self, request, view, obj):
        if request.user.role == 'admin':
            return True
        return obj.user == request.user
