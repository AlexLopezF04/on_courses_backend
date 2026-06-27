from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsOwnerOrAdminForReview(BasePermission):
    """Solo el autor de la reseña o un admin pueden modificarla."""
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.user == request.user or request.user.role == 'admin'
