from rest_framework.routers import DefaultRouter
from tasks.views.task_views import TaskViewSet
from tasks.views.category_views import CategoryViewSet

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'categories', CategoryViewSet, basename='category-list')

urlpatterns = router.urls