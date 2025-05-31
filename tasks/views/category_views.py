from injector import inject
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from tasks.serializers import CategorySerializer
from tasks.services.interfaces import ICategoryService


class CategoryViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for managing task categories.
    Provides CRUD operations for categories.
    Requires authentication.
    """
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    @inject
    def setup(self, request, *args, category_service: ICategoryService, **kwargs):
        """
        Initializes the ViewSet and injects the CategoryService.

        Args:
            request: The HTTP request object.
            category_service (ICategoryService): The category service injected by django-injector.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super().setup(request, *args, **kwargs)
        self.category_service = category_service

    def get_queryset(self):
        """
        Returns the queryset of all categories.
        (Consider filtering by user if categories are user-specific).
        """
        return self.category_service.get_all_categories()

    def perform_create(self, serializer):
        """
        Performs the creation of a new category, assigning a random color.

        Args:
            serializer: The serializer instance containing validated data.
        """
        color = self.category_service.assign_random_color_to_category()
        serializer.save(color=color)