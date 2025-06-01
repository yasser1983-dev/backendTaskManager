from rest_framework.pagination import PageNumberPagination

class CustomTaskPagination(PageNumberPagination):
    """
    Custom pagination class for TaskViewSet.
    Sets a specific page size for tasks.
    """
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100  # Maximum page size allowed if client overrides