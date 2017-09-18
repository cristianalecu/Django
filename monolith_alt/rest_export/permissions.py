from rest_framework import permissions

class CanModifyOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow staff to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions are only allowed to the staff.
        return request.user and request.user.is_staff;
    
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS or
            request.user and
            request.user.is_staff
        )