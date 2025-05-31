from tasks.models import Task
from tasks.services.interfaces import ITaskService


class TaskService(ITaskService):

    def get_user_tasks(self, user):
        """
        Retrieves all tasks for a given user, ordered by creation date descending.
        """
        return Task.objects.filter(user=user).order_by('-created_at')

    def get_pending_tasks(self, user, limit=6):
        """
        Retrieves a limited number of pending tasks for a given user,
        ordered by creation date descending.
        """
        return Task.objects.filter(user=user, status='pending').order_by('-created_at')[:limit]

    def get_completed_tasks(self, user, limit=6):
        """
        Retrieves a limited number of completed tasks for a given user,
        ordered by creation date descending.
        """
        return Task.objects.filter(user=user, status='completed').order_by('-created_at')[:limit]

    def mark_task_as_completed(self, task_id, user):
        """
        Marks a specific task as completed for a given user.
        Returns the updated task object or None if the task is not found.
        """
        try:
            task = Task.objects.get(pk=task_id, user=user)
            task.status = 'completed'
            task.save()
            return task
        except Task.DoesNotExist:
            return None
