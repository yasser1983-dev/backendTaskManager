import pytest
from django.utils import timezone
from tasks.models import Category
from tasks.services.category_service import CategoryService

@pytest.mark.django_db
class TestCategoryServiceIntegration:

    def test_get_all_categories_returns_sorted_queryset(self):
        timestamp = int(timezone.now().timestamp())
        category_b = Category.objects.create(name=f"TestB_{timestamp}", color="#00897B")
        category_a = Category.objects.create(name=f"TestA_{timestamp}", color="#3949AB")
        category_c = Category.objects.create(name=f"TestC_{timestamp}", color="#E53935")

        service = CategoryService()
        categories_queryset = service.get_all_categories()

        category_names = list(categories_queryset.values_list('name', flat=True))

        assert f"TestA_{timestamp}" in category_names
        assert f"TestB_{timestamp}" in category_names
        assert f"TestC_{timestamp}" in category_names

        expected_sorted_test_names = [f"TestA_{timestamp}", f"TestB_{timestamp}", f"TestC_{timestamp}"]

        found_test_names_in_order = [
            name for name in category_names if name in expected_sorted_test_names
        ]

        assert found_test_names_in_order == expected_sorted_test_names


    def test_assign_random_color_to_category_returns_available_color(self):
        Category.objects.create(name="Existing", color="#00897B")

        service = CategoryService()
        color = service.assign_random_color_to_category()

        assert color != "#00897B"
        assert color in [
            '#E53935', '#8E24AA', '#3949AB', '#039BE5',
            '#43A047', '#FDD835', '#FB8C00', '#D81B60'
        ]

    def test_assign_random_color_to_category_all_colors_used(self):
        colors = ['#E53935', '#8E24AA', '#3949AB', '#039BE5',
                  '#00897B', '#43A047', '#FDD835', '#FB8C00', '#D81B60']
        for i, color in enumerate(colors):
            Category.objects.create(name=f"Cat{i}", color=color)

        service = CategoryService()
        color = service.assign_random_color_to_category()

        assert color in colors
