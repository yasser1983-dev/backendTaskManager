from injector import inject
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from tasks.services.auth_service import AuthService


class LogoutViewSet(viewsets.ViewSet):
    """
    A ViewSet for handling user logout.
    Requires authentication to log out.
    """
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'], url_path='logout')
    @inject
    def logout(self, request, auth_service: AuthService):
        """
        Logs out the current user by deleting their authentication token.

        Args:
            request: The HTTP request object.
            auth_service (AuthService): The authentication service injected by django-injector.

        Returns:
            Response: A DRF Response indicating logout success or failure.
        """
        if auth_service.logout_user(request.user):
            return Response({"detail": "Logged out successfully"}, status=status.HTTP_200_OK)
        return Response({"detail": "Logout failed or no token found."}, status=status.HTTP_400_BAD_REQUEST)