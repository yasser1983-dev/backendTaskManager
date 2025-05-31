# tasks/tests/unit/test_category_viewset_unit.py

import pytest
from rest_framework.test import APIRequestFactory
from unittest.mock import Mock

from tasks.views.category_views import CategoryViewSet
from tasks.serializers import CategorySerializer
from tasks.models import Category


@pytest.mark.django_db
def test_get_queryset_returns_categories():
    service_mock = Mock()
    service_mock.get_all_categories.return_value = Category.objects.all()

    request = APIRequestFactory().get('/api/categories/')
    view = CategoryViewSet()
    view.setup(request, category_service=service_mock)

    queryset = view.get_queryset()

    service_mock.get_all_categories.assert_called_once()
    assert list(queryset) == list(Category.objects.all())


@pytest.mark.django_db
def test_perform_create_assigns_random_color():
    color = "#43A047"
    service_mock = Mock()
    service_mock.assign_random_color_to_category.return_value = color

    serializer_mock = Mock()
    view = CategoryViewSet()
    view.setup(APIRequestFactory().post('/api/categories/'), category_service=service_mock)

    view.perform_create(serializer_mock)

    serializer_mock.save.assert_called_once_with(color=color)
