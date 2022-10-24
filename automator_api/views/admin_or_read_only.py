from rest_framework.permissions import IsAdminUser, SAFE_METHODS


class IsAdminOrReadOnly(IsAdminUser):
    """Permission class to keep non-admin users from making post, update, or delete requests
    """

    def has_permission(self, request, view):
        is_admin = super().has_permission(request, view)
        return request.method in SAFE_METHODS or is_admin
