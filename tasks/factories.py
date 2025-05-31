from tasks.services.interfaces import ITaskService
from tasks.services.task_service import TaskService
from tasks.services.category_service import CategoryService

class ServiceFactory:
    @staticmethod
    def get_task_service() -> ITaskService:
        return TaskService()

class CategoryServiceFactory:
    @staticmethod
    def get_category_service():
        return CategoryService()


class AbstractServiceFactory:
    @staticmethod
    def get_factory(factory_type: str):
        if factory_type == "task":
            return ServiceFactory()
        elif factory_type == "category":
            return CategoryServiceFactory()
        else:
            raise ValueError(f"Unknown factory type: {factory_type}")

