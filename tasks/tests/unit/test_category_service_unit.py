from unittest.mock import patch


class TestCategoryServiceUnit:
    """
    Tests unitarios para CategoryService.
    Estos tests no interactúan con la base de datos real, usando mocks en su lugar.
    """

    @patch('tasks.services.category_service.Category.objects')
    def test_assign_random_color_to_category_with_available_colors(self, mock_category_objects, category_service_instance):
        """
        Verifica que assign_random_color_to_category devuelve un color disponible
        cuando hay colores que no están en uso.
        """
        mock_category_objects.values_list.return_value = ['#E53935', '#8E24AA']

        service = category_service_instance
        result = service.assign_random_color_to_category()

        assert result in [
            '#3949AB', '#039BE5', '#00897B', '#43A047',
            '#FDD835', '#FB8C00', '#D81B60'
        ]
        mock_category_objects.values_list.assert_called_once_with('color', flat=True)

    @patch('tasks.services.category_service.Category.objects')
    def test_assign_random_color_to_category_all_used(self, mock_category_objects, category_service_instance):
        """
        Verifica que assign_random_color_to_category devuelve un color (incluso si está usado)
        cuando todos los colores predefinidos ya están en uso.
        """
        mock_category_objects.values_list.return_value = [
            '#E53935', '#8E24AA', '#3949AB', '#039BE5',
            '#00897B', '#43A047', '#FDD835', '#FB8C00', '#D81B60'
        ]

        service = category_service_instance
        result = service.assign_random_color_to_category()

        assert result in [
            '#E53935', '#8E24AA', '#3949AB', '#039BE5',
            '#00897B', '#43A047', '#FDD835', '#FB8C00', '#D81B60'
        ]
        mock_category_objects.values_list.assert_called_once_with('color', flat=True)

    @patch('tasks.services.category_service.Category.objects')
    def test_get_all_categories_orders_by_name(self, mock_category_objects, category_service_instance):
        """
        Test unitario para get_all_categories, verificando que llama a order_by('name').
        """
        service = category_service_instance
        service.get_all_categories()

        mock_category_objects.all.assert_called_once()

        mock_category_objects.all.return_value.order_by.assert_called_once_with('name')