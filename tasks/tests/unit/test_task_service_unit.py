from unittest.mock import MagicMock

from django.contrib.auth import get_user_model

from tasks.models import Task


def test_get_user_tasks_unit(task_service_instance, mocker):
    """
    Unit test for get_user_tasks, mocking the Django ORM calls.
    """
    mock_user = MagicMock(spec=get_user_model())
    expected_tasks = [MagicMock(spec=Task), MagicMock(spec=Task)]

    # Mock the entire chain: Task.objects.filter(...).order_by(...)
    mocker.patch(
        'tasks.models.Task.objects.filter',
        return_value=MagicMock(order_by=MagicMock(return_value=expected_tasks))
    )

    result = task_service_instance.get_user_tasks(mock_user)

    Task.objects.filter.assert_called_once_with(user=mock_user)
    Task.objects.filter.return_value.order_by.assert_called_once_with('-created_at')
    assert result == expected_tasks


def test_get_pending_tasks_unit(task_service_instance, mocker):
    """
    Unit test for get_pending_tasks, mocking the Django ORM calls.
    """
    mock_user = MagicMock(spec=get_user_model())
    expected_tasks = [MagicMock(spec=Task)]

    mock_ordered_queryset = MagicMock()
    mock_ordered_queryset.__getitem__.return_value = expected_tasks # Mock the slice operation
    mocker.patch(
        'tasks.models.Task.objects.filter',
        return_value=MagicMock(order_by=MagicMock(return_value=mock_ordered_queryset))
    )

    result = task_service_instance.get_pending_tasks(mock_user, limit=6)

    Task.objects.filter.assert_called_once_with(user=mock_user, status='pending')
    Task.objects.filter.return_value.order_by.assert_called_once_with('-created_at')
    mock_ordered_queryset.__getitem__.assert_called_once_with(slice(None, 6, None))
    assert result == expected_tasks


def test_get_completed_tasks_unit(task_service_instance, mocker):
    """
    Unit test for get_completed_tasks, mocking the Django ORM calls.
    """
    mock_user = MagicMock(spec=get_user_model())
    expected_tasks = [MagicMock(spec=Task), MagicMock(spec=Task)]

    mock_ordered_queryset = MagicMock()
    mock_ordered_queryset.__getitem__.return_value = expected_tasks
    mocker.patch(
        'tasks.models.Task.objects.filter',
        return_value=MagicMock(order_by=MagicMock(return_value=mock_ordered_queryset))
    )

    result = task_service_instance.get_completed_tasks(mock_user, limit=6)

    Task.objects.filter.assert_called_once_with(user=mock_user, status='completed')
    Task.objects.filter.return_value.order_by.assert_called_once_with('-created_at')
    mock_ordered_queryset.__getitem__.assert_called_once_with(slice(None, 6, None))
    assert result == expected_tasks


def test_mark_task_as_completed_unit_success(task_service_instance, mocker):
    """
    Unit test for mark_task_as_completed when task is found and updated.
    Mocks the Django ORM calls.
    """
    mock_task_instance = MagicMock(spec=Task)
    mock_task_instance.status = 'pending' # Initial state
    mock_task_instance.pk = 1
    mock_task_objects_get = mocker.patch('tasks.models.Task.objects.get', return_value=mock_task_instance)
    mock_user = MagicMock(spec=get_user_model())

    result = task_service_instance.mark_task_as_completed(1, mock_user)

    mock_task_objects_get.assert_called_once_with(pk=1, user=mock_user)
    assert mock_task_instance.status == 'completed'
    mock_task_instance.save.assert_called_once()
    assert result == mock_task_instance


def test_mark_task_as_completed_unit_not_found(task_service_instance, mocker):
    """
    Unit test for mark_task_as_completed when task is not found.
    Mocks the Django ORM calls.
    """
    mocker.patch('tasks.models.Task.objects.get', side_effect=Task.DoesNotExist)
    mock_user = MagicMock(spec=get_user_model())

    result = task_service_instance.mark_task_as_completed(999, mock_user)

    assert result is None


def test_mark_task_as_completed_unit_wrong_user(task_service_instance, mocker):
    """
    Unit test for mark_task_as_completed when task exists but belongs to another user.
    Mocks the Django ORM calls (simulate DoesExist for wrong user query).
    """
    mocker.patch('tasks.models.Task.objects.get', side_effect=Task.DoesNotExist)
    mock_user = MagicMock(spec=get_user_model()) # User trying to access
    mock_other_user_task_id = 123 # A task ID belonging to another user

    result = task_service_instance.mark_task_as_completed(mock_other_user_task_id, mock_user)

    assert result is None
    Task.objects.get.assert_called_once_with(pk=mock_other_user_task_id, user=mock_user)
