import datetime

import pytest
from django.utils import timezone

from tasks.models import Task
from tasks.services.task_service import TaskService


# Instantiate the service once for all tests in this module
@pytest.fixture(scope='module')
def task_service_instance():
    """Provides an instance of TaskService."""
    return TaskService()

@pytest.mark.django_db
def test_get_user_tasks_integration(task_service_instance, common_user, other_user, task_factory):
    """
    Integration test for get_user_tasks, ensuring it interacts correctly with the DB.
    """
    task1 = task_factory(user=common_user, title='Task 1', created_at=timezone.now() - datetime.timedelta(days=2))
    task2 = task_factory(user=common_user, title='Task 2', created_at=timezone.now() - datetime.timedelta(days=1))
    task_factory(user=other_user, title='Other User Task') # Should not be included

    tasks = task_service_instance.get_user_tasks(common_user)

    assert len(tasks) == 2
    assert tasks[0] == task2 # Ordered by created_at descending
    assert tasks[1] == task1


@pytest.mark.django_db
def test_get_pending_tasks_integration(task_service_instance, common_user, task_factory):
    """
    Integration test for get_pending_tasks, ensuring it interacts correctly with the DB.
    """
    task1 = task_factory(user=common_user, title='Pending 1', status='pending', created_at=timezone.now() - datetime.timedelta(days=2))
    task2 = task_factory(user=common_user, title='Completed 1', status='completed', created_at=timezone.now() - datetime.timedelta(days=3))
    task3 = task_factory(user=common_user, title='Pending 2', status='pending', created_at=timezone.now() - datetime.timedelta(days=1))

    pending_tasks = task_service_instance.get_pending_tasks(common_user, limit=2)

    assert len(pending_tasks) == 2
    assert pending_tasks[0] == task3 # Ordered by created_at descending
    assert pending_tasks[1] == task1
    assert task2 not in pending_tasks


@pytest.mark.django_db
def test_get_completed_tasks_integration(task_service_instance, common_user, task_factory):
    """
    Integration test for get_completed_tasks, ensuring it interacts correctly with the DB.
    """
    task1 = task_factory(user=common_user, title='Pending 1', status='pending', created_at=timezone.now() - datetime.timedelta(days=2))
    task2 = task_factory(user=common_user, title='Completed 1', status='completed', created_at=timezone.now() - datetime.timedelta(days=3))
    task3 = task_factory(user=common_user, title='Completed 2', status='completed', created_at=timezone.now() - datetime.timedelta(days=1))

    completed_tasks = task_service_instance.get_completed_tasks(common_user, limit=2)

    assert len(completed_tasks) == 2
    assert completed_tasks[0] == task3 # Ordered by created_at descending
    assert completed_tasks[1] == task2
    assert task1 not in completed_tasks


@pytest.mark.django_db
def test_mark_task_as_completed_integration_success(task_service_instance, common_user, task_factory):
    """
    Integration test for mark_task_as_completed, ensuring it updates the DB correctly.
    """
    task = task_factory(user=common_user, title='Task to complete', status='pending')

    updated_task = task_service_instance.mark_task_as_completed(task.pk, common_user)

    assert updated_task is not None
    assert updated_task.pk == task.pk
    assert updated_task.status == 'completed'
    # Verify by fetching from DB again
    refreshed_task = Task.objects.get(pk=task.pk)
    assert refreshed_task.status == 'completed'


@pytest.mark.django_db
def test_mark_task_as_completed_integration_not_found(task_service_instance, common_user):
    """
    Integration test for mark_task_as_completed when task does not exist in DB.
    """
    result = task_service_instance.mark_task_as_completed(999, common_user)
    assert result is None


@pytest.mark.django_db
def test_mark_task_as_completed_integration_wrong_user(task_service_instance, common_user, other_user, task_factory):
    """
    Integration test for mark_task_as_completed when task belongs to another user.
    """
    task_other_user = task_factory(user=other_user, title='Task for other user')

    result = task_service_instance.mark_task_as_completed(task_other_user.pk, common_user)
    assert result is None
    # Ensure the task status for the other user's task remains unchanged
    refreshed_task = Task.objects.get(pk=task_other_user.pk)
    assert refreshed_task.status == 'pending' # It should still be pending