from injector import inject
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from tasks.serializers import TaskSerializer, CategorySerializer
from tasks.services.interfaces import ITaskService, ICategoryService
from tasks.pagination import CustomTaskPagination

class TaskViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for managing user tasks.
    Provides CRUD operations for tasks and custom actions for filtering.
    Requires authentication.
    """
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomTaskPagination

    @inject
    def setup(self, request, *args, task_service: ITaskService, **kwargs):
        """
        Initializes the ViewSet and injects the TaskService.

        Args:
            request: The HTTP request object.
            task_service (ITaskService): The task service injected by django-injector.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super().setup(request, *args, **kwargs)
        self.task_service = task_service

    def get_queryset(self):
        """
        Returns the queryset of tasks specific to the authenticated user.
        """
        return self.task_service.get_user_tasks(self.request.user)

    def perform_create(self, serializer):
        """
        Performs the creation of a new task, associating it with the current user.

        Args:
            serializer: The serializer instance containing validated data.
        """
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'], url_path='pending')
    def pending(self, request):
        """
        Retrieves all pending tasks for the authenticated user.

        Args:
            request: The HTTP request object.

        Returns:
            Response: A DRF Response containing serialized pending tasks.
        """
        tasks = self.task_service.get_pending_tasks(user=request.user)
        if tasks is not None:
            serializer = self.get_serializer(tasks, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='completed')
    def completed(self, request):
        """
        Retrieves all completed tasks for the authenticated user.

        Args:
            request: The HTTP request object.

        Returns:
            Response: A DRF Response containing serialized completed tasks.
        """
        tasks = self.task_service.get_completed_tasks(user=request.user)
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['patch'], url_path='mark-completed')
    def mark_completed(self, request, pk=None):
        """
        Marks a specific task as completed.

        Args:
            request: The HTTP request object.
            pk (int): The primary key of the task to mark as completed.

        Returns:
            Response: A DRF Response with the serialized updated task or an error if not found.
        """
        task = self.task_service.mark_task_as_completed(pk, request.user)
        if not task:
            return Response({"detail": "Task not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(task)
        return Response(serializer.data)