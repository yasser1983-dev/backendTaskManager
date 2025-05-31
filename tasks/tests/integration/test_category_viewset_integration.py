import uuid

import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from tasks.models import Category


@pytest.mark.django_db
def test_list_categories_authenticated():
    # 1. Setup - Clear existing data and create test data
    Category.objects.all().delete()

    user = User.objects.create_user(username="testuser", password="12345")
    category1 = Category.objects.create(name="Trabajo 1", color="#00897B")
    category2 = Category.objects.create(name="Personal 1", color="#3949AB")

    client = APIClient()
    client.force_authenticate(user=user)

    response = client.get('/api/categories/', format='json')

    assert response.status_code == 200
    assert isinstance(response.data, dict)
    assert response.data['count'] == 2
    assert len(response.data['results']) == 2

    returned_names = {item['name'] for item in response.data['results']}
    assert returned_names == {"Personal 1", "Trabajo 1"}


@pytest.mark.django_db
def test_create_category_assigns_color():
    user = User.objects.create_user(username="testuser", password="12345")

    unique_name = f"TestCategoria-{uuid.uuid4().hex[:6]}"
    client = APIClient()
    client.force_authenticate(user=user)

    response = client.post('/api/categories/', {'name': unique_name}, format='json')

    assert response.status_code == 201
    assert Category.objects.filter(name=unique_name).exists()
    assert Category.objects.get(name=unique_name).color is not None
