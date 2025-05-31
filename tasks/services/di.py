from injector import Module, provider, singleton
from .interfaces import ITaskService, ICategoryService
from .task_service import TaskService
from .category_service import CategoryService

class TaskModule(Module):
    @provider
    @singleton
    def provide_task_service(self) -> ITaskService:
        return TaskService()

class CategoryModule(Module):
    @provider
    @singleton
    def provide_category_service(self) -> ICategoryService:
        return CategoryService()
