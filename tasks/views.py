from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from tasks.models import Task, Category
from tasks.serializers import TaskSerializer, CategorySerializer
from tasks.task_service import assign_random_color_to_category


class LogoutViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'], url_path='logout')
    def logout(self, request):
        # Elimina el token asociado al usuario autenticado
        request.user.auth_token.delete()
        return Response({"detail": "Logged out successfully"}, status=status.HTTP_200_OK)

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'], url_path='pending')
    def pending(self, request):
        queryset = self.get_queryset().filter(status='pending')[:6]
        return Response(TaskSerializer(queryset, many=True).data)

    @action(detail=False, methods=['get'], url_path='completed')
    def completed(self, request):
        queryset = self.get_queryset().filter(status='completed')[:6]
        return Response(TaskSerializer(queryset, many=True).data)

    @action(detail=True, methods=['patch'], url_path='mark-completed')
    def mark_completed(self, request, pk=None):
        task = self.get_object()
        task.status = 'completed'
        task.save()
        return Response(TaskSerializer(task).data)


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Category.objects.all()

    def perform_create(self, serializer):
        color = assign_random_color_to_category()
        serializer.save(color=color)
