from rest_framework import permissions

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Only allow owners of the object (Order) or admin to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # SAFE_METHODS allowed to anyone with view permission
        if request.method in permissions.SAFE_METHODS:
            return True
        # obj has user attr (Order)
        return getattr(obj, "user", None) == request.user or request.user.is_staff
