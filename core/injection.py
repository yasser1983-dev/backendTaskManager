from injector import Injector, Module, singleton, Binder

from tasks.services.auth_service import AuthService
from tasks.services.interfaces import ITaskService, ICategoryService, IAuthService
from tasks.services.task_service import TaskService
from tasks.services.category_service import CategoryService

class AppModule(Module):
    def configure(self, binder: Binder):
        binder.bind(ITaskService, to=TaskService, scope=singleton)
        binder.bind(ICategoryService, to=CategoryService, scope=singleton)
        binder.bind(IAuthService, to=AuthService, scope=singleton)

injector = Injector([AppModule()])
